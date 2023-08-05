from abc import ABC, abstractmethod

from symbot.control.control import Control


class BaseMedia(ABC):
    """Abstract base class to implement new commands

    Abstract base class developers need to implement for new commands.
    Enforces all properties and methods required by controller.

    Attributes
    ----------
    control : Control
        central control element
    name : str
        media identifier (default: module name)
    author : str
        author identifier (default: None)
    permission_level : int
        permission level of media (default: public)
    cooldown : float
        minimum seconds between command calls (default: 0)
    enabled : bool
        command is enabled

    Methods
    -------
    run
        execute media under consideration of arguments
    """

    def __init__(self, control: Control):
        self.control = control
        self.name = self.__module__.split('.')[-1]
        self.author = ''
        self.permission_level = 3
        self.cooldown = 0
        self.enabled = True

    @abstractmethod
    async def run(self, **kwargs):
        """execute media under consideration of arguments

        Parameters
        ----------
        kwargs : dict
            key-worded arguments
        """
        ...
