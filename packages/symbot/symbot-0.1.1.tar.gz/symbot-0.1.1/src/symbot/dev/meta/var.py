import logging

from symbot.chat.message import Message
from symbot.dev.meta._base_meta_command import BaseMetaCommand


class Command(BaseMetaCommand):
    """Manipulate variables in the environment

    Methods
    -------
    run
        execute when !var is called
    getvar
        retrieve variable from environment
    setvar
        edit a command
    delvar
        delete a command
    """

    def __init__(self, control):
        super().__init__(control)
        self.name = '!var'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        try:
            operation = msg.context[0]
        except IndexError:
            logging.info(f'{self.name} missing operation argument')
            return

        if operation == 'get':
            await self.getvar(msg)
        elif operation == 'set':
            await self.setvar(msg)
        elif operation == 'del':
            await self.delvar(msg)
        else:
            logging.info(f'{self.name} encountered an undefined operation argument {operation}')

    async def getvar(self, msg):
        """retrieve variable from environment

        Parameters
        ----------
        msg : Message
            user message trying to retrieve a variable
        """

        try:
            var = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} missing context var')
            return
        try:
            val = self.control.environment.get(var)
        except KeyError:
            logging.info(f'{self.name} unable to find var {var}')
            return

        response = f'{var} has value {val}'
        await self.control.respond(response)

    async def setvar(self, msg):
        """set value of a variable

        Parameters
        ----------
        msg : Message
            user message trying to set the value of a variable
        """

        try:
            var = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} missing context var')
            return
        try:
            new_value = msg.context[2]
        except IndexError:
            logging.info(f'{self.name} missing context value')
            return
        self.control.environment.set(var, new_value)

        response = f'value of {var} has been changed to {new_value}'
        await self.control.respond(response)

    async def delvar(self, msg):
        """delete a variable from the environment

        Parameters
        ----------
        msg : Message
            message containing var to be deleted
        """

        try:
            var = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} missing context var')
            return
        try:
            self.control.environment.delete(var)
        except KeyError:
            logging.info(f'{self.name} unable to find var {var}')
            return

        response = f'{var} has been deleted'
        await self.control.respond(response)
