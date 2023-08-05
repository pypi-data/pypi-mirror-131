import asyncio
import logging
import os
import sys
from importlib import import_module
from os.path import join

from symbot.config import dev_path
from symbot.control.auxiliary.cooldowns import Cooldowns
from symbot.control.auxiliary.environment import Environment
from symbot.control.auxiliary.permissions import Permissions
from symbot.control.auxiliary.settings import Settings


class Control:
    """Central control element

    Controller communicates between Twitch chat, various data files,
    media elements and command calls & responses. Dynamically loads
    commands from dev and utilizes auxiliary controllers.

    Attributes
    ----------
    permissions : Permissions
        checks user permission levels
    environment : Environment
        manages environmental variables
    cooldowns : Cooldowns
        tracks command cooldowns
    settings : Settings
        overrides default command settings
    media : dict
        dict of all media loaded dynamically
    commands : list
        dict of all commands loaded dynamically
    msg_queue : Queue
        thread safe queue to receive Twitch messages
    resp_queue : Queue
        thread safe queue to push responses to

    Methods
    -------
    import_media
        recursively import and instantiate all media in a directory
    get_media
        try to find media by name
    import_commands
        recursively import and instantiate all commands in a directory
    delete_command
        delete command from dict and unload module
    get_command
        try to find command by name
    requeue
        push message back to message queue
    respond
        push response to response queue
    process
        continuously process messages from Twitch channel
    """

    def __init__(self):

        # dynamically load in media
        self.media = {}
        logging.info('loading media')
        self.import_media(join(dev_path, 'media'))

        # dynamically load in commands
        self.commands = {}
        logging.info('loading commands')
        self.import_command(join(dev_path, 'commands'))
        self.import_command(join(dev_path, 'meta'))

        # auxiliary controllers
        self.permissions = Permissions()
        self.environment = Environment()
        self.cooldowns = Cooldowns()
        self.settings = Settings(self.commands)

        # async data structures
        self.msg_queue = None
        self.resp_queue = asyncio.Queue()

    def import_media(self, path):
        """recursively import and instantiate all media in a directory

        Parameters
        ----------
        path : str
            current directory of modules to be imported
        """

        splits = path.split(os.sep)
        file = splits[-1]
        # exclude files not meant to be imported as command
        if file.startswith('_'):
            return
        # import .py module
        elif file.endswith('.py'):
            module = file[:-3]
            for m in splits[::-1][1:]:
                module = '.'.join([m, module])
                if m == 'symbot':
                    break
            media = import_module(module).Media(self)
            self.media[media.name] = media
        # import package
        else:
            for file in os.listdir(path):
                # import modules from lower levels recursively
                self.import_media(join(path, file))

    def get_media(self, media_name):
        """try to find media by name

        Parameters
        ----------
        media_name : str
            media identifier

        Returns
        -------
        Media
            desired media, or None if not found
        """

        if media_name not in self.media:
            return None
        return self.media[media_name]

    def import_command(self, path):
        """recursively import and instantiate all commands in a directory

        Parameters
        ----------
        path : str
            current directory of modules to be imported
        """

        splits = path.split(os.sep)
        file = splits[-1]
        # exclude files not meant to be imported as command
        if file.startswith('_'):
            return
        # import .py module
        elif file.endswith('.py'):
            module = file[:-3]
            for m in splits[::-1][1:]:
                module = '.'.join([m, module])
                if m == 'symbot':
                    break
            command = import_module(module).Command(self)
            self.commands[command.name] = command
        # import package
        else:
            for file in os.listdir(path):
                # import modules from lower levels recursively
                self.import_command(join(path, file))

    def delete_command(self, command):
        """delete command from dict and unload module

        Parameters
        ----------
        command : Command
            command to be deleted
        """

        del self.commands[command.name]
        sys.modules.pop(command.__module__)

    def get_command(self, cmd_name):
        """try to find command by name

        Parameters
        ----------
        cmd_name : str
            command identifier

        Returns
        -------
        Command
            desired command, or None if not found
        """

        if cmd_name not in self.commands:
            return None
        return self.commands[cmd_name]

    async def requeue(self, msg):
        """push message back to message queue

        Parameters
        ----------
        msg : Message
            modified message that needs to be reprocessed
        """
        await self.msg_queue.put(msg)

    async def respond(self, response):
        """push response to response queue

        Parameters
        ----------
        response : str
            response to be sent to Twitch channel
        """

        await self.resp_queue.put(response)

    async def process(self):
        """continuously process messages from Twitch channel

        continuously process messages from Twitch channel. Check for
        various flags before executing a command. Not every command
        generates a response.
        """

        # run forever
        while True:
            # wait for message to process
            # provided by chat
            msg = await self.msg_queue.get()
            command = self.get_command(msg.command)
            # check for existence
            if not command:
                continue
            # check if command is enabled
            if not command.enabled:
                logging.info(f'{command.name} is disabled')
                continue
            # check for permission
            if not self.permissions.check_call(command.permission_level, msg.user):
                logging.info(f'{msg.user} has insufficient permission to call {command.name}')
                continue
            # check for cooldown
            if self.cooldowns.has_cooldown(command, msg.timestamp):
                logging.info(f'{command.name} is still on cooldown')
                continue
            # command is safe to execute
            # append command to asyncio loop
            asyncio.get_running_loop().create_task(command.run(msg))
