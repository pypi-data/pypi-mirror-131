import logging

from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!highfive'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        try:
            recipient = msg.context[0]
        except IndexError:
            logging.info(f'{self.name} missing context recipient')
            return
        user = msg.user

        response = f'{user} gave {recipient} a highfive!'
        await self.control.respond(response)
