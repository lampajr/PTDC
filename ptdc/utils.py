import time


def get_millis():

    """ returns the current time in milliseconds """

    return int(round(time.time() * 1000))


def get_time():

    """ returns the current time in seconds """

    return int(round(time.time()))