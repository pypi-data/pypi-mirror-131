import json
import logging
from os.path import join

from symbot.config import data_path
from symbot.util.updater import update_json


class Permissions:
    """Controller class for user permission levels

    user permission levels as of now:
        0 : broadcaster
        1 : moderator
        2 : whitelisted
        3 : default
        4 : blacklisted

    Attributes
    ----------
    file_path : str
        path of datafile
    permissions : dict
        dict to store user permission levels

    Methods
    -------
    set
        assign permission level to a user
    get
        retrieve user permission level
    check_call
        determine whether user has sufficient permission to call a command
    check_meta
        determine whether user has sufficient permission to modify a command
    """

    def __init__(self):

        # MAYBE put path into config or somewhere else
        self.file_path = join(data_path, 'user_permissions.json')

        # load permissions from data folder
        try:
            logging.info('loading user permissions')
            with open(self.file_path) as file:
                self.permissions = json.load(file)
        # or start a fresh environment
        except FileNotFoundError:
            logging.info(f'no permissions found in {self.file_path}')
            self.permissions = {}
            logging.info('created new user permissions')

    def set(self, user, level):
        """assign permission level to a user

        Parameters
        ----------
        user : str
            user identifier
        level : int
            permission level
        """

        if level == 3:
            del self.permissions[user]
        else:
            self.permissions[user] = level
        update_json(self.permissions, self.file_path)

    def get(self, user):
        """retrieve user permission level

        Parameters
        ----------
        user : str
            user identifier

        Returns
        -------
        int
            user permission level
        """

        if user in self.permissions:
            # get user level from data
            return self.permissions[user]
        else:
            # or use default permission level
            # MAYBE enable dev user levels from config
            # MAYBE use enumerate?
            return 3

    def check_call(self, cmd_level, user):
        """determine whether user has sufficient permission to call a command

        Parameters
        ----------
        cmd_level : int
            minimum permission level required by command
        user : str
            user name

        Returns
        -------
        bool
            user has sufficient permission
        """

        return self.get(user) <= cmd_level

    def check_meta(self, cmd_level, user):
        """determine whether user has sufficient permission to modify a command

        Parameters
        ----------
        cmd_level : int
            minimum permission level required by command
        user : str
            user name

        Returns
        -------
        bool
            user has sufficient permission
        """

        return self.get(user) < cmd_level
