import time
from datetime import datetime


def get_time(millis=False):

    """
    Returns current time
    :param millis: if True returns current time in millis, else in seconds
    :returns: the current time in seconds/millis
    """

    t = time.time()

    if millis:
        return int(round(t * 1000))
    else:
        return int(round(t))


def get_date(format_="%b %d %Y %H:%M:%S"):

    """
    Returns the current date
    :param format_: date format, example '%Y-%m-%d'"""

    return datetime.today().strftime(format_)


def get_attribute(obj, attr_name):

    """
    Retrieve the attribute of a specific object
    :param obj: object from which get the value
    :param attr_name: name of the attribute
    :return: value of the attribute
    """

    return getattr(obj, attr_name)

def get_media(status):

    """
    Retrieve media urls of a tweet
    :param status: Tweet object
    :return: urls list or None
    """

    try:
        return [med["url"] for med in status.entities["media"]]
    except KeyError:
        return None


def get_quoted_user_id(status):

    """
    Retrieve the user id of the original tweet
    :param status: Tweet object
    :return: user id or None
    """

    try:
        return status.quoted_status.user.id if status.is_quote_status else None
    except AttributeError:
        return None

def get_retweeted_user_id(status):

    """
    Retrieve the user id of the original status
    :param status: Tweet object
    :return: user id or None
    """

    try:
        return status.retweeted_status.user.id
    except AttributeError:
        return None

def get_retweeted_status(status):

    """
    Retrieve the id of the retweeted status
    :param status: Tweet object
    :return: status id or None
    """

    try:
        return status.retweeted_status.id
    except AttributeError:
        return None
