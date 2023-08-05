import logging

from symbot.chat.message import Message
from symbot.dev.meta._base_meta_command import BaseMetaCommand
from symbot.util import updater


class Command(BaseMetaCommand):
    """Purge all commands created by a specified user"""

    def __init__(self, control):
        super().__init__(control)
        self.name = '!purge'
        self.author = 'fd_symbicort'
        self.permission_level = 0

    async def run(self, msg: Message):

        try:
            user = msg.context[0]
        except IndexError:
            logging.info(f'{self.name} missing context user name')
            return

        # gather commands created by user
        commands = [command for command in self.control.commands.values() if command.author == user]

        # if any such commands exist
        if commands:

            for command in commands:
                # delete command from control
                self.control.delete_command(command)
                # delete file containing command
                updater.delete_command_file(command)

            command_names = ', '.join([command.name for command in commands])

            response = f'Purged commands: {command_names} of user {user}'
        else:
            response = f'{user} has not created any commands'

        await self.control.respond(response)
