from abc import ABC, abstractmethod

from symbot.chat.message import Message
from symbot.control.control import Control


class BaseCommand(ABC):
    """Abstract base class to implement new commands

    Abstract base class developers need to implement for new commands.
    Enforces all properties and methods required by controller.

    Attributes
    ----------
    control : Control
        central control element
    name : str
        command identifier (default: module name)
    author : str
        author identifier (default: None)
    permission_level : int
        permission level of command (default: public)
    cooldown : float
        minimum seconds between command calls (default: 0)
    enabled : bool
        command is enabled

    Methods
    -------
    run
        execute command under consideration of user message
    """

    def __init__(self, control: Control):
        self.control = control
        self.name = self.__module__.split('.')[-1]
        self.author = ''
        self.permission_level = 3
        self.cooldown = 0
        self.enabled = True

    @abstractmethod
    async def run(self, msg: Message):
        """execute command under consideration of user message

        Parameters
        ----------
        msg : Message
            message sent by user
        """
        ...
