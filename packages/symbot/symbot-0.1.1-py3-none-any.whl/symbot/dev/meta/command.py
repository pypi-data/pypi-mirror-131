import logging
import re

from symbot.chat.message import Message
from symbot.dev.meta._base_meta_command import BaseMetaCommand
from symbot.dev.meta._builder import Builder
from symbot.util import updater
from symbot.util.strings import stringify


class Command(BaseMetaCommand):
    """Central meta command

    Add, Edit or Delete commands and their files with !command

    Methods
    -------
    run
        execute when !command is called
    addcom
        add a new command
    editcom
        edit a command
    delcom
        delete a command
    skellify_message
        parse message to blueprint of a command
    skellify_command
        parse command to blueprint of a command
    """

    def __init__(self, control):
        super().__init__(control)
        self.name = '!command'
        self.author = 'fd_symbicort'

        self.builder = Builder(control)

        # filter string escapes
        self.msg_filter = re.compile('[\'\"\\\]')

        # message extractors
        self.arg_extractor = re.compile('\\$(.*){(.*)}')
        self.setting_extractor = re.compile('-(.*)=(.*)')

        # file extractors
        self.r_extractor = re.compile(r'response = f\'(.*)\'')
        self.v_extractor = re.compile(r'get\(\'(\w*)\'\)')
        self.c_extractor = re.compile(r'increment\(\'(\w*)\'\)')
        self.a_extractor = re.compile(r' (\w*) = msg\.context\[\d\]')
        self.u_extractor = re.compile(r' (\w*) = msg\.user')
        self.alias_extractor = re.compile(r'msg\.command = \'(\S*)\'')
        self.name_extractor = re.compile(r'name = (\S*)')
        self.author_extractor = re.compile(r'author = (\S*)')
        self.permission_level_extractor = re.compile(r'permission_level = (\S*)')
        self.cooldown_extractor = re.compile(r'cooldown = (\S*)')
        self.enabled_extractor = re.compile(r'enabled = (\S*)')

    async def run(self, msg: Message):

        try:
            operation = msg.context[0]
        except IndexError:
            logging.info(f'{self.name} missing operation argument')
            return

        if operation == 'add':
            await self.addcom(msg)
        elif operation == 'edit':
            await self.editcom(msg)
        elif operation == 'del':
            await self.delcom(msg)
        else:
            logging.info(f'{self.name} encountered an undefined operation argument {operation}')

    async def addcom(self, msg):
        """add a new command

        Parameters
        ----------
        msg : Message
            user message trying to add a new command
        """

        # extract command name
        try:
            name = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} add missing command name argument')
            return
        if self.control.get_command(name):
            logging.info(f'{self.name} add {name} already exists')
            return
        try:
            msg.context[2]
        except IndexError:
            logging.info(f'{self.name} add {name} missing content')
            return

        # create command blueprint
        skeleton = self.skellify_message(msg, name, 'add')
        if skeleton:
            # create command, load it and respond
            self.builder.create_command(skeleton)
            await self.control.respond(f'{msg.user} has added {name} to commands')

    async def editcom(self, msg):
        """edit a command

        Parameters
        ----------
        msg : Message
            user message trying to edit a command
        """

        # extract command name
        try:
            name = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} edit missing command name argument')
            return
        if not self.control.get_command(name):
            logging.info(f'{self.name} edit {name} does not exist')
            return
        try:
            msg.context[2]
        except IndexError:
            logging.info(f'{self.name} edit {name} missing content')
            return

        # skellify message and command
        skeleton_message = self.skellify_message(msg, name, 'edit')
        file = updater.get_file_by_command(self.control.get_command(msg.context[1]))
        skeleton_command = self.skellify_command(file)

        # check if only settings are being edited
        # do not change response in that case
        only_settings = True
        for k, v in skeleton_message.items():
            if k != 'settings' and v:
                only_settings = False
                break

        # overwrite settings
        del skeleton_message['settings']['name']
        del skeleton_message['settings']['author']
        for setting, value in skeleton_message['settings'].items():
            skeleton_command['settings'][setting] = value
        del skeleton_message['settings']

        # overwrite response
        if not only_settings:
            for k, v in skeleton_message.items():
                skeleton_command[k] = v

        # edit command, reload it and respond
        self.builder.edit_command(self.control.get_command(name), skeleton_command, file)
        await self.control.respond(f'{msg.user} has modified command {name}')

    async def delcom(self, msg):
        """delete a command

        Parameters
        ----------
        msg : Message
            message containing command to be deleted
        """

        # extract command name
        try:
            name = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} del missing command name argument')
            return
        command = self.control.get_command(name)
        if not command:
            logging.info(f'{self.name} del {name} does not exists')
            return

        # check for safety conditions
        # MAYBE increase security
        if self.control.permissions.check_meta(command.permission_level, msg.user) \
                or command.author == msg.user:
            # delete command and respond
            self.builder.delete_command(command)
            await self.control.respond(f'{msg.user} has removed command {name}')

    def skellify_message(self, msg, name, operation):
        """parse message to blueprint of a command

        Parameters
        ----------
        msg : Message
            message to be parsed
        name : str
            command name
        operation : str
            command operation for logging

        Returns
        -------
        dict
            blueprint of a command
        """

        # blueprint container
        skeleton = {
            # response
            'r': [],
            # variables
            'v': [],
            # counters
            'c': [],
            # arguments
            'a': [],
            # user
            'u': [],
            # alias
            'alias': [],
            # settings
            'settings': {'name': stringify(name), 'author': stringify(msg.user)}
        }

        # start parsing after command name
        for s in msg.context[2:]:

            # filter string escapes [' " \] for security
            s = self.msg_filter.sub('', s)

            # $ indicates special item
            if s.startswith('$'):
                try:
                    # extract special item
                    arg, value = self.arg_extractor.search(s).groups()
                    skeleton[arg].append(value)
                    skeleton['r'].append('{' + value + '}')
                except AttributeError:
                    logging.info(f'{self.name} {operation} {name} has bad argument')
                    return
                except KeyError:
                    logging.info(f'{self.name} {operation} {name} encountered undefined argument')
                    return
            # - indicates setting
            elif s.startswith('-'):
                try:
                    # extract setting
                    setting, value = self.setting_extractor.search(s).groups()
                    if setting == 'ul':
                        skeleton['settings']['permission_level'] = int(value)
                    elif setting == 'cd':
                        skeleton['settings']['cooldown'] = float(value)
                    elif setting == 'on':
                        skeleton['settings']['enabled'] = value.lower() == 'true'
                    else:
                        logging.info(f'{self.name} {operation} {name} invalid setting {setting}')
                        return
                except AttributeError:
                    logging.info(f'{self.name} {operation} {name} has bad setting')
                    return
                except ValueError:
                    logging.info(f'{self.name} {operation} {name} can not convert setting value')
                    return
            else:
                skeleton['r'].append(s)

        # if parsing was successful, return blueprint
        # otherwise null was already returned
        return skeleton

    def skellify_command(self, path):
        """parse command to blueprint of a command

        Parameters
        ----------
        path : str
            absolute path of module containing command

        Returns
        -------
        dict
            blueprint of a command
        """

        with open(path, 'r') as f:
            code = f.read()

        skeleton = {}

        response = self.r_extractor.findall(code)
        if response:
            skeleton['r'] = response[0].split(' ')
        else:
            skeleton['r'] = []

        # variables
        skeleton['v'] = self.v_extractor.findall(code)
        # counters
        skeleton['c'] = self.c_extractor.findall(code)
        # arguments
        skeleton['a'] = self.a_extractor.findall(code)
        # user
        skeleton['u'] = self.u_extractor.findall(code)
        # alias
        skeleton['alias'] = self.alias_extractor.findall(code)

        skeleton['settings'] = {}

        name = self.name_extractor.findall(code)
        if name:
            skeleton['settings']['name'] = name[0]
        author = self.author_extractor.findall(code)
        if author:
            skeleton['settings']['author'] = author[0]
        permission_level = self.permission_level_extractor.findall(code)
        if permission_level:
            skeleton['settings']['permission_level'] = permission_level
        cooldown = self.cooldown_extractor.findall(code)
        if cooldown:
            skeleton['settings']['cooldown'] = cooldown
        enabled = self.enabled_extractor.findall(code)
        if enabled:
            skeleton['settings']['enabled'] = enabled

        return skeleton
