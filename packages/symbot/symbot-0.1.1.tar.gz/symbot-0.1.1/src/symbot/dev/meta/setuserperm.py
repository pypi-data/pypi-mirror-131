import logging

from symbot.chat.message import Message
from symbot.dev.meta._base_meta_command import BaseMetaCommand


class Command(BaseMetaCommand):

    def __init__(self, control):
        super().__init__(control)
        self.name = '!setuserperm'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        try:
            user = msg.context[0]
        except IndexError:
            logging.info(f'{self.name} missing context user')
            return
        try:
            new_value = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} missing context value')
            return
        try:
            if not int(new_value) in [0, 1, 2, 3, 4]:
                logging.info(f'{self.name} requires value in [0, 1, 2, 3, 4]')
                return
        except ValueError:
            logging.info(f'{self.name} requires value in [0, 1, 2, 3, 4]')
            return
        self.control.permissions.set(user, int(new_value))

        response = f'{user} has now permission level {new_value}'
        await self.control.respond(response)
