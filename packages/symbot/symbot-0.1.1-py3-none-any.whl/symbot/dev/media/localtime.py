from symbot.control.control import Control
from symbot.dev.media._base_media import BaseMedia

import time


class Media(BaseMedia):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = 'localtime'
        self.author = 'fd_symbicort'

    async def run(self, **kwargs):
        return time.strftime('%I:%M %p', time.localtime(time.time()))
