from time import time


class Cooldowns:
    """Controller class to keep track of command cooldowns

    Attributes
    ----------
    cooldowns : dict([Command, float])
        dict to keep track of command cooldowns

    Methods
    -------
    has_cooldown
        determine whether a command is on cooldown
    """

    def __init__(self):
        self.cooldowns = dict()

    def has_cooldown(self, command, msg_timestamp):
        """determine whether a command is on cooldown

        Parameters
        ----------
        command : Command
            command to be checked for cooldown
        msg_timestamp : float
            epoch time of message

        Returns
        -------
        bool
            command is on cooldown
        """

        # check for existing entry
        if command in self.cooldowns:
            # if less time since last call has passed than cooldown
            if msg_timestamp - self.cooldowns[command] < command.cooldown:
                return True
        # if command was not on cooldown, put on cooldown
        self.cooldowns[command] = time()
        return False
