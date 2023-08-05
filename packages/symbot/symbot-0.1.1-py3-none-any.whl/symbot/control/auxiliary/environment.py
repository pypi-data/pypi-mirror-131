import json
import logging
from os.path import join

from symbot.config import data_path
from symbot.util.updater import update_json


class Environment:
    """Controller class for Twitch chat's environmental variables

    Attributes
    ----------
    environment : dict
        dict to store environmental variables

    Methods
    -------
    get
        get the value of a variable
    set
        set the value of a variable
    initialize
        initialize new variable as 0 if it doesn't exist yet
    increment
        increment the value of a variable
    delete
        delete variable from environment
    """

    def __init__(self):

        # MAYBE put path into config or somewhere else
        self.file_path = join(data_path, 'environment.json')

        # load environment from data folder
        try:
            logging.info('loading environment')
            with open(self.file_path) as file:
                self.environment = json.load(file)
        # or start a fresh environment
        except FileNotFoundError:
            logging.info(f'no environment found in {self.file_path}')
            self.environment = {}
            logging.info('created new environment')

    def get(self, var):
        """get the value of a variable

        Parameters
        ----------
        var : str
            variable name identifying desired value

        Returns
        -------
        object
            desired value
        """

        # handle var not defined in command
        return self.environment[var]

    def set(self, var, val):
        """set the value of a variable

        Parameters
        ----------
        var : str
            variable name identifying value
        val : object
            value to be set

        Returns
        -------
        object
            set value
        """

        # if var already exists, typecast new value to old type
        if var in self.environment:
            val = type(self.environment[var])(val)
        # if var is a digit, typecast to int
        elif type(val) == str:
            if val.isdigit():
                val = int(val)

        self.environment[var] = val
        update_json(self.environment, self.file_path)
        return val

    def initialize(self, var):
        """initialize new variable as 0 if it doesn't exist yet

        Parameters
        ----------
        var : str
            variable to be initiated
        """

        if var not in self.environment:
            self.set(var, 0)

    def increment(self, var):
        """increment the value of a variable

        Parameters
        ----------
        var : str
            variable name identifying value to be incremented

        Returns
        -------
        int
            incremented value
        """

        # handle var not defined in command
        self.environment[var] += 1
        update_json(self.environment, self.file_path)
        return self.environment[var]

    def delete(self, var):
        """delete variable from environment

        Parameters
        ----------
        var : str
            variable to be deleted from environment
        """

        del self.environment[var]
