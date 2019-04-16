import pandas as pd
import numpy as np


_all_user_attributes = np.array(["id", "name", "screen_name", "location", "url", "description", "protected",
                                 "verified", "followers_count", "friends_count", "listed_count", "favourites_count",
                                 "statuses_count", "created_at", "utc_offset", "geo_enabled", "lang",
                                 "contributors_enabled", "profile_background_color", "profile_background_image_url",
                                 "profile_background_image_url_https", "profile_background_tile",
                                 "profile_image_url", "profile_image_url_https", "profile_link_color",
                                 "profile_text_color", "profile_use_background_image", "default_profile",
                                 "default_profile_image"])

_new_user_attributes = np.array(["profile_crawled", "is_suspended"])

_all_tweets_attributes = np.array([])

_new_tweets_attributes = np.array([])

_user_attr_size = len(_all_user_attributes) + len(_new_user_attributes)
_tweet_attr_size = len(_all_tweets_attributes) + len(_new_tweets_attributes)


def create_twitter_account_dataframe(selectors):

    """ Create an empty pandas DataFrame with specified attributes, suitable for storing user's information
    :param selectors: Numpy array of booleans that tells which attribute keep, default: all True
    """

    # keep only the attributes for which the boolean is set to True
    _attributes = np.concatenate((_all_user_attributes, _new_user_attributes), axis=0)[selectors]

    # create empty DataFrame with specified attributes
    _dataset = pd.DataFrame(columns=_attributes)
    return _dataset


def create_twitter_tweets_dataframe(selectors):

    """ Create an empty pandas DataFrame with specified attributes, suitable for storing tweet's information
    :param selectors: Numpy array of booleans that tells which attribute keep, default: all True
    """

    # keep only the attributes for which the boolean is set to True
    _attributes = np.concatenate((_all_tweets_attributes, _new_tweets_attributes), axis=0)[selectors]

    # create empty DataFrame with specified attributes
    _dataset = pd.DataFrame(columns=_attributes)
    return _dataset


"""
User object structure
{
 'follow_request_sent': False, 
 'profile_use_background_image': True, 
 'id': 132728535, 
 '_api': <tweepy.api.api object="" at="" xxxxxxx="">, 
 'verified': False, 
 'profile_sidebar_fill_color': 'C0DFEC', 
 'profile_text_color': '333333', 
 'followers_count': 80, 
 'protected': False, 
 'location': 'Seoul Korea', 
 'profile_background_color': '022330', 
 'id_str': '132728535', 
 'utc_offset': 32400, 
 'statuses_count': 742, 
 'description': "Cars, Musics, Games, Electronics, toys, food, etc... I'm just a typical boy!",
 'friends_count': 133, 
 'profile_link_color': '0084B4', 
 'profile_image_url': 'http://a1.twimg.com/profile_images/1213351752/_2_2__normal.jpg',
 'notifications': False, 
 'show_all_inline_media': False, 
 'geo_enabled': True, 
 'profile_background_image_url': 'http://a2.twimg.com/a/1294785484/images/themes/theme15/bg.png',
 'screen_name': 'jaeeeee', 
 'lang': 'en', 
 'following': True, 
 'profile_background_tile': False, 
 'favourites_count': 2, 
 'name': 'Jae Jung Chung', 
 'url': 'http://www.carbonize.co.kr', 
 'created_at': datetime.datetime(2010, 4, 14, 1, 20, 45), 
 'contributors_enabled': False, 
 'time_zone': 'Seoul', 
 'profile_sidebar_border_color': 'a8c7f7', 
 'is_translator': False, 
 'listed_count': 2
}
"""

class DataCollector(object):

    """ Data Collector that stores the accounts dataset:
    provides methods for handling the data, adding new users, removing users.."""

    def __init__(self, api, user_attrs_selectors=None, tweets_attrs_selectors=None):
        self._user_attrs_selectors = np.ones(_user_attr_size, dtype=bool) if user_attrs_selectors is None else \
            user_attrs_selectors
        self._tweets_attrs_selectors = np.ones(_tweet_attr_size, dtype=bool) if tweets_attrs_selectors is None else \
            tweets_attrs_selectors

        # empty datasets
        self._user_dataset = create_twitter_account_dataframe(selectors=self._user_attrs_selectors)
        self._tweets_dataset = create_twitter_tweets_dataframe(selectors=self._tweets_attrs_selectors)

        # Twitter api for making query
        self._api = api

    def get_data(self):

        """ return the pandas DataFrame"""

        return self._user_dataset

    def add_user(self, screen_name):
        user = self._api.get_user(screen_name)

        # TODO: collect timeline of user

        # retrieve all information about single user
        raw_data = pd.Series([getattr(user, attr) for attr in _all_user_attributes], index=self._user_dataset.columns)

        # TODO: add new attributes data, manually
        raw_data = raw_data[self._user_attrs_selectors]
        self._user_dataset = self._user_dataset.append(raw_data, ignore_index=True)


    def to_csv(self, filename):
        self._user_dataset.to_csv(path_or_buf=filename, index=False)