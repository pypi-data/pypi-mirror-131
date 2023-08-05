from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!commands'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):
        response = f'https://github.com/tobi208/symbot#commands'
        await self.control.respond(response)
