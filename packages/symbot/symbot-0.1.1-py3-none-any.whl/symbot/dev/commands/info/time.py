import logging

from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!time'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        localtime = self.control.get_media('localtime')

        if localtime:

            try:
                broadcaster = self.control.environment.get('broadcaster')
            except KeyError:
                logging.info(f'{self.name} unable to find var broadcaster')
                return

            response = f'It is {await localtime.run()} for {broadcaster}'

            await self.control.respond(response)

        else:

            logging.info('Required media unavailable: localtime')
