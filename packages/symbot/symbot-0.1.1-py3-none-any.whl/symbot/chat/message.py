import re
import time


class Message:
    """Represents a message received from Twitch as workable object

    Attributes
    ----------
    user : str
        user who sent the message
    channel : str
        channel message was sent to
    timestamp: float
        time since epoch
    content : str
        actual message sent by user
    command : str
        command identifier
    context : str
        context to a command
    """

    def __init__(self, received):
        """
        Parameters
        ----------
         received : str
            private message from Twitch channel
        """

        # regex parser that works on private messages from twitch channel
        # MAYBE try/catch for correct input just in case
        # MAYBE expand to generic messages
        groups = re.search(
            ':(.*)!.*@.*\.tmi\.twitch\.tv PRIVMSG (#.*)? :(.*)',
            received).groups()

        self.user = groups[0]
        self.channel = groups[1]
        self.timestamp = time.time()
        self.content = groups[2]
        # extract command and context from content
        split = self.content.split(' ')
        self.command = split[0]
        self.context = split[1:]
