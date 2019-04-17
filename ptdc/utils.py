import time
from datetime import datetime

def get_millis():

    """ returns the current time in milliseconds """

    return int(round(time.time() * 1000))


def get_time():

    """ returns the current time in seconds """

    return int(round(time.time()))

def get_date():

    """ returns the current date """

    return datetime.today().strftime('%Y-%m-%d')