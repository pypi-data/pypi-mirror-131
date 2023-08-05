import logging

from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!good'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):
        try:
            good = self.control.environment.increment('good')
        except KeyError:
            logging.info(f'{self.name} unable to find var good')
            return
        try:
            broadcaster = self.control.environment.get('broadcaster')
        except KeyError:
            logging.info(f'{self.name} unable to find var broadcaster')
            return

        response = f'{broadcaster} has done {good} things well'
        await self.control.respond(response)
