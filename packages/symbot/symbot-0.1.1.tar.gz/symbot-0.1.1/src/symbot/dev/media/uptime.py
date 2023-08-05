from symbot.control.control import Control
from symbot.dev.media._base_media import BaseMedia

from time import time


class Media(BaseMedia):
    """Trace time since chat bot was started"""

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = 'uptime'
        self.author = 'fd_symbicort'
        self.start = time()

    async def run(self, **kwargs):
        return int(time() - self.start)
