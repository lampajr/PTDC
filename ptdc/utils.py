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

def get_media(tweet, attr_name):

    """
    Retrieve media urls of a tweet
    :param tweet: Tweet object
    :param attr_name: unused
    :return: urls list or None
    """

    try:
        return [med["url"] for med in tweet.entities["media"]]
    except KeyError:
        return None


def get_quoted_user_id(tweet, attr_name):

    """
    Retrieve the user id of the original tweet
    :param tweet: Tweet object
    :param attr_name: unused
    :return: user id or None
    """

    try:
        return tweet.quoted_status.user.id if tweet.is_quote_status else None
    except AttributeError:
        return None


# DEFAULT COLLECTOR DATA


DEFAULT_N_TWEETS = 20


default_user_dict = {"id": get_attribute,
                     "name": get_attribute,
                     "screen_name": get_attribute,
                     "location": get_attribute,
                     "url": get_attribute,
                     "description": get_attribute,
                     "protected": get_attribute,
                     "verified": get_attribute,
                     "followers_count": get_attribute,
                     "friends_count": get_attribute,
                     "listed_count": get_attribute,
                     "favourites_count": get_attribute,
                     "statuses_count": get_attribute,
                     "created_at": get_attribute,
                     "utc_offset": get_attribute,
                     "time_zone": get_attribute,
                     "geo_enabled": get_attribute,
                     "lang": get_attribute,
                     "contributors_enabled": get_attribute,
                     "profile_background_color": get_attribute,
                     "profile_background_image_url": get_attribute,
                     "profile_background_image_url_https": get_attribute,
                     "profile_background_tile": get_attribute,
                     "profile_image_url": get_attribute,
                     "profile_image_url_https": get_attribute,
                     "profile_link_color": get_attribute,
                     "profile_text_color": get_attribute,
                     "profile_use_background_image": get_attribute,
                     "default_profile": get_attribute,
                     "default_profile_image": get_attribute,
                     "profile_crawled": lambda x, y: get_date(),
                     "is_suspended": lambda x, y: 0,
                     "f_ratio (following/follower)": lambda user, _: user.friends_count / user.followers_count}

default_user_tweets_dict = {"n_tweets_collected": lambda statuses_data, _: statuses_data.shape[0],
                            "mean_tweet_length": lambda statuses_data, _: statuses_data["text_length"].mean(),
                            "quoted_user_ids": lambda statuses_data, _: statuses_data["quoted_user_id"],
                            "replied_status_ids": lambda statuses_data, _: statuses_data["in_reply_to_status_id"],
                            "replied_user_ids": lambda statuses_data, _: statuses_data["in_reply_to_user_id"]}

default_tweet_dict = {"id": get_attribute,
                      "created_at": get_attribute,
                      "full_text": get_attribute,
                      "lang": get_attribute,
                      "coordinates": get_attribute,
                      "retweet_count": get_attribute,
                      "favorite_count": get_attribute,
                      "source": get_attribute,
                      "place": get_attribute,
                      "truncated": get_attribute,
                      "is_quote_status": get_attribute,
                      "in_reply_to_status_id": get_attribute,
                      "in_reply_to_user_id": get_attribute,
                      "in_reply_to_screen_name": get_attribute,
                      "user_id": lambda status, _: status.user.id,
                      "text_length": lambda status, _: len(status.full_text),
                      "hashtags": lambda status, _: [ht["text"] for ht in status.entities["hashtags"]],
                      "media_urls": get_media,
                      "quoted_user_id": get_quoted_user_id}
