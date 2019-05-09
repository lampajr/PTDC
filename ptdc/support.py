"""
Support module provides useful function used for computing attributes and other things

:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""

import time
from datetime import datetime

import tweepy


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


def get_country(status):

    """
    Retrieve the country from a Place object
    :param status: status obj
    :return: country's place
    """
    try:
        place = status.place
        if place is None:
            return None
        return place.country
    except KeyError:
        return None


def get_place_type(status):

    """
    Retrieve the place type from a Place object
    :param status: status obj
    :return: place type, like city
    """

    try:
        place = status.place
        if place is None:
            return None
        return place.place_type
    except KeyError:
        return None


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


def authenticate(consumer_key,
                 consumer_key_secret,
                 access_token,
                 access_token_secret,
                 host='api.twitter.com',
                 search_host='search.twitter.com',
                 upload_host='upload.twitter.com',
                 cache=None, api_root='/1.1',
                 search_root='', upload_root='/1.1',
                 retry_count=0,
                 retry_delay=0, retry_errors=None,
                 timeout=60, parser=None,
                 compression=False,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True,
                 proxy=''):

    """
    Helpful method that allow user to directly authenticate and generate the API for querying Twitter

    Authentication tokens:_auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    _auth.set_access_token(access_token, access_token_secret)
    _api = tweepy.API(auth_handler=_auth,
                      host=host,
                      search_host=search_host,
                      upload_host=upload_host,
                      cache=cache,
                      api_root=api_root,
                      search_root=search_root,
                      upload_root=upload_root,
                      retry_count=retry_count,
                      retry_delay=retry_delay,
                      retry_errors=retry_errors,
                      timeout=timeout,
                      parser=parser,
                      compression=compression,
                      wait_on_rate_limit=wait_on_rate_limit,
                      wait_on_rate_limit_notify=wait_on_rate_limit_notify,
                      proxy=proxy)
    :param consumer_key:
    :param consumer_key_secret:
    :param access_token:
    :param access_token_secret:

    API parameters, for a more detailed description see Tweepy API documentation
    :param host:
    :param search_host:
    :param upload_host:
    :param cache:
    :param api_root:
    :param search_root:
    :param upload_root:
    :param retry_count:
    :param retry_delay:
    :param retry_errors:
    :param timeout:
    :param parser:
    :param compression:
    :param wait_on_rate_limit:
    :param wait_on_rate_limit_notify:
    :param proxy:
    :return: Tweepy API object
    """

    _auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    _auth.set_access_token(access_token, access_token_secret)
    _api = tweepy.API(auth_handler=_auth,
                      host=host,
                      search_host=search_host,
                      upload_host=upload_host,
                      cache=cache,
                      api_root=api_root,
                      search_root=search_root,
                      upload_root=upload_root,
                      retry_count=retry_count,
                      retry_delay=retry_delay,
                      retry_errors=retry_errors,
                      timeout=timeout,
                      parser=parser,
                      compression=compression,
                      wait_on_rate_limit=wait_on_rate_limit,
                      wait_on_rate_limit_notify=wait_on_rate_limit_notify,
                      proxy=proxy)
    return _api
