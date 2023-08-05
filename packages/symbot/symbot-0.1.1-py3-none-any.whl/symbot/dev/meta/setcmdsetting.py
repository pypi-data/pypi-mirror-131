import logging

from symbot.chat.message import Message
from symbot.dev.meta._base_meta_command import BaseMetaCommand


class Command(BaseMetaCommand):

    def __init__(self, control):
        super().__init__(control)
        self.name = '!setcmdsetting'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        try:
            name = msg.context[0]
        except IndexError:
            logging.info(f'{self.name} missing context command name')
            return
        try:
            setting = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} missing context setting')
            return
        try:
            value = msg.context[2]
        except IndexError:
            logging.info(f'{self.name} missing context value')
            return

        if self.control.settings.set(name, setting, value):
            response = f'Changed {setting} of {name} to value {value}'
            await self.control.respond(response)
