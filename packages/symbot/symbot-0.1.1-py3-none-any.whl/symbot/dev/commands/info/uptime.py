import logging

from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!uptime'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        uptime = self.control.get_media('uptime')

        if uptime:

            elapsed = await uptime.run()

            seconds = elapsed % 60
            elapsed = (elapsed - seconds) / 60
            minutes = int(elapsed) % 60
            elapsed = (elapsed - minutes) / 60
            hours = int(elapsed) % 24
            elapsed = (elapsed - hours) / 24
            days = int(elapsed)

            time_str = ''
            if seconds > 0:
                time_str = f' {seconds} s'
            if minutes > 0:
                time_str = f' {minutes} m' + time_str
            if hours > 0:
                time_str = f' {hours} h' + time_str
            if days > 0:
                time_str = f' {days} d' + time_str

            response = f'Stream has been live for{time_str}'

            await self.control.respond(response)

        else:

            logging.info('Required media unavailable: uptime')
