"""Utility to manipulate strings

Methods
-------
stringify
     wraps string in apostrophes

"""


def stringify(s):
    """wraps string in apostrophes

    Parameters
    ----------
    s : str
        string to be wrapped in apostrophes

    Returns
    -------
    str
        string wrapped in apostrophes
    """
    return '\'' + s + '\''
