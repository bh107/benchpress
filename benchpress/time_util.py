# -*- coding: utf-8 -*-

import datetime


def time2str(time_obj):
    """Convert a `datetype` object to a string.

    Parameters
    ----------
    time_obj : datetime.datetype
        The time object to convert
        
    Returns
    -------
    time : str
        A string representing the datetime.
    """
    return time_obj.isoformat()


def str2time(time_str):
    """Convert a string to a `datetime` object.

    Parameters
    ----------
    time_str : str
        The string to convert to `datetime.datetime`

    Returns
    -------
    time : datetime.datetime
        A datetime object representing the `time_str`.
    """
    return datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")


def utcnow_str():
    """ Return a new datetime string representing UTC day and time. """
    return time2str(datetime.datetime.utcnow())
