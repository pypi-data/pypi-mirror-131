import json
import os

from os.path import abspath, join

"""Utility to update files when data changes

MAYBE make oop instead of static
MAYBE use multiprocessing

Methods
-------
update_json
    update json file with data from dictionary
write_file
    write file
delete_file
    delete file
delete_command_file
    delete file containing command
get_file_by_command
    get file containing command
"""


def update_json(dictionary, file_path):
    """update json file with data from dictionary

    Parameters
    ----------
    dictionary : dict
        dict containing updated data
    file_path : str
        path of file to be updated
    """

    with open(file_path, 'w') as file:
        json.dump(dictionary, file, indent=2)


def write_file(content, file_path):
    """write file

    Parameters
    ----------
    content : str
        content of file
    file_path : str
        relative file path
    """
    with open(file_path, 'w') as file:
        file.write(content)


def delete_file(file):
    """delete file

    Parameters
    ----------
    file : str
        file to be deleted
    """

    os.remove(file)


def delete_command_file(command):
    """delete file containing command

    Parameters
    ----------
    command : Command
        command contained by file to be deleted
    """

    delete_file(get_file_by_command(command))


def get_file_by_command(command):
    """get file containing command

    Parameters
    ----------
    command : Command
        command contained by file
    """

    return join(*abspath(command.__module__).split('.')) + '.py'
