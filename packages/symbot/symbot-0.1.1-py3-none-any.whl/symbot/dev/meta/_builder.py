import re
from os.path import join

from symbot.util import updater
from symbot.util.strings import stringify
from symbot.config import dev_path


class Builder:
    """ Builder to assemble or reassemble commands, write files and load them

    Methods
    -------
    create_command
        creates command from a skeleton as file and loads it
    edit_command
        recreates command from a skeleton as file and reloads it
    delete_command
        deletes command and unloads it
    assemble
        assembles command code from skeleton
    """

    def __init__(self, control):
        self.control = control

    def create_command(self, skeleton):
        """creates command from a skeleton as file and loads it

        Parameters
        ----------
        skeleton : dict
            blueprint containing all information about the command
        """

        # assemble command
        code = self.assemble(skeleton)
        file_name = re.search(r'\w+', skeleton['settings']['name']).group(0)
        file_path = join(dev_path, 'commands', 'new', file_name + '.py')
        # write file
        updater.write_file(code, file_path)
        # load command
        self.control.import_command(file_path)

    def edit_command(self, command, skeleton, path):
        """recreates command from a skeleton as file and reloads it

        Parameters
        ----------
        command : Command
            command to be edited
        skeleton : dict
            blueprint containing all information about the command
        path : str
            file path of module containing command
        """

        # assemble command
        code = self.assemble(skeleton)
        # rewrite file
        updater.write_file(code, path)
        # reload command
        self.control.delete_command(command)
        self.control.import_command(path)

    def delete_command(self, command):
        """deletes command and unloads it

        Parameters
        ----------
        command : Command
            command to be deleted
        """

        # delete file
        updater.delete_command_file(command)
        # unload command
        self.control.delete_command(command)

    def assemble(self, skeleton):
        """assembles command code from skeleton

        Parameters
        ----------
        skeleton : dict
            blueprint containing all information about the command
        """

        # header always the same
        code = \
            'import logging\n' \
            '\n' \
            'from symbot.chat.message import Message\n' \
            'from symbot.control.control import Control\n' \
            'from symbot.dev.commands._base_command import BaseCommand\n' \
            '\n' \
            '\n' \
            'class Command(BaseCommand):\n' \
            '\n' \
            '    def __init__(self, control: Control):\n' \
            '        super().__init__(control)\n'

        # override default settings
        for setting, value in skeleton['settings'].items():
            code += \
                f'        self.{setting} = {value}\n'

        code += \
            '\n' \
            '    async def run(self, msg: Message):\n'

        # adjust message according to alias
        for alias in skeleton['alias']:
            code += \
                '\n' \
                f'        msg.command = {stringify(alias)}\n' \
                '\n' \
                '        await self.control.requeue(msg)\n'

        # aliases are special case
        # ignore everything else and
        # only execute aliases
        # MAYBE change in the future
        if len(skeleton['alias']) > 0:
            return code

        # initialize var if it does not exist
        # increment vars
        for var in skeleton['c']:
            self.control.environment.initialize(var)
            code += \
                '        try:\n' \
                f'            {var} = self.control.environment.increment({stringify(var)})\n' \
                '        except KeyError:\n' \
                f'            logging.info(f\'{{self.name}} unable to find var {var}\')\n' \
                '            return\n'

        # initialize var if it does not exist
        # retrieve vars
        for var in skeleton['v']:
            self.control.environment.initialize(var)
            code += \
                '        try:\n' \
                f'            {var} = self.control.environment.get({stringify(var)})\n' \
                '        except KeyError:\n' \
                f'            logging.info(f\'{{self.name}} unable to find var {var}\')\n' \
                '            return\n'

        # retrieve arguments from message
        for i, arg in enumerate(skeleton['a']):
            code += \
                '        try:\n' \
                f'            {arg} = msg.context[{i}]\n' \
                '        except IndexError:\n' \
                f'            logging.info(f\'{{self.name}} missing context {arg}\')\n' \
                '            return\n'

        # retrieve user from message
        for user in skeleton['u']:
            code += \
                f'        {user} = msg.user\n'

        # generate response
        response = ' '.join(skeleton['r'])
        code += \
            '\n' \
            f'        response = f\'{response}\'\n'

        # respond to control
        code += \
            '        await self.control.respond(response)\n'

        return code
