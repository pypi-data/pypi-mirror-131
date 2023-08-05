import logging

from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!bad'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):
        try:
            bad = self.control.environment.increment('bad')
        except KeyError:
            logging.info(f'{self.name} unable to find var bad')
            return
        try:
            broadcaster = self.control.environment.get('broadcaster')
        except KeyError:
            logging.info(f'{self.name} unable to find var broadcaster')
            return

        response = f'{broadcaster} has done {bad} things poorly'
        await self.control.respond(response)
