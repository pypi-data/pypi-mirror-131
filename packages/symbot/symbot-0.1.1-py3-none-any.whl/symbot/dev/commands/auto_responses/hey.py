from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = 'hey'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        recipient = msg.user

        response = f'Hello there, {recipient} HeyGuys'
        await self.control.respond(response)
