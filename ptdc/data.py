import pandas as pd
import numpy as np


_all_attributes = np.array(["id", "name", "screen_name", "location", "url", "description", "derived", "protected",
                            "verified", "followers_count", "friends_count", "listed_count", "favourites_count",
                            "statuses_count", "created_at", "geo_enabled", "lang", "contributors_enabled",
                            "profile_background_color", "profile_background_image_url",
                            "profile_background_image_url_https", "profile_background_tile", "profile_banner_url",
                            "profile_image_url", "profile_image_url_https", "profile_link_color",
                            "profile_text_color", "profile_use_background_image", "default_profile",
                            "default_profile_image"])

_size = len(_all_attributes)


def create_twitter_account_dataframe(selectors=None):

    """ Create an empty pandas DataFrame with specified attributes, suitable for storing user's information
    :param selectors: Numpy array of booleans that tells which attribute keep, default: all True
    """

    # keep only the attributes for which the boolean is set to True
    _selectors = np.ones(_size, dtype=bool) if selectors is None else selectors
    _attributes = _all_attributes[_selectors]

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

class UserDataCollector(object):

    """ Data Collector that stores the accounts dataset:
    provides methods for handling the data, adding new users, removing users.."""

    def __init__(self, api, selectors=None):
        self._dataset = create_twitter_account_dataframe(selectors=selectors)
        self._api = api

    def add_user(self, screen_name):
        user = self._api.get_user(screen_name)