import logging

import pandas as pd
import numpy as np
import tweepy

from ptdc import utils

_all_user_attributes = np.array(["id", "name", "screen_name", "location", "url", "description", "protected",
                                 "verified", "followers_count", "friends_count", "listed_count", "favourites_count",
                                 "statuses_count", "created_at", "utc_offset", "time_zone", "geo_enabled", "lang",
                                 "contributors_enabled", "profile_background_color", "profile_background_image_url",
                                 "profile_background_image_url_https", "profile_background_tile",
                                 "profile_image_url", "profile_image_url_https", "profile_link_color",
                                 "profile_text_color", "profile_use_background_image", "default_profile",
                                 "default_profile_image"])

_new_user_attributes = np.array(["profile_crawled", "is_suspended", "n_tweets_collected", "mean_tweet_length"])

_all_tweets_attributes = np.array(["id", "created_at", "full_text", "lang", "coordinates", "retweet_count",
                                   "favorite_count", "source", "place", "truncated", "is_quote_status",
                                   "possibly_sensitive", "in_reply_to_status_id", "in_reply_to_user_id",
                                   "in_reply_to_screen_name"])

_new_tweets_attributes = np.array(["user_id", "text_length", "hashtags", "media_urls", "quoted_user_id"])


# attributes' sizes

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


class DataCollector(object):

    """ Data Collector that stores the DataFrames of the account and/or their tweets:
    provides methods for handling the data, adding new users, removing users.."""

    def __init__(self, api, user_attrs_selectors=None, collect_users=True,
                 tweets_attrs_selectors=None, collect_tweets=True, verbose=True):
        self.verbose = verbose
        self._collect_tweets = collect_tweets
        self._collect_users = collect_users
        self._user_attrs_selectors = np.ones(_user_attr_size, dtype=bool) if user_attrs_selectors is None else \
            user_attrs_selectors
        self._tweets_attrs_selectors = np.ones(_tweet_attr_size, dtype=bool) if tweets_attrs_selectors is None else \
            tweets_attrs_selectors

        # empty datasets
        self._user_dataset = create_twitter_account_dataframe(selectors=self._user_attrs_selectors)
        self._tweets_dataset = create_twitter_tweets_dataframe(selectors=self._tweets_attrs_selectors)

        # Twitter api for making query
        self._api = api

    def get_users_dataset(self):

        """ Return pandas DataFrame containing collected accounts"""

        return self._user_dataset

    def get_tweets_dataset(self):

        """ Returns pandas DataFrame containing collected tweets"""

        return self._tweets_dataset

    # USERS

    def collect_user(self, screen_name):

        """ Collect all the information about a specific Account
        :param screen_name: the screen_name/id of the account"""

        user = self._api.get_user(screen_name)

        if self.verbose:
            logging.debug("Collecting user {}".format(screen_name))

        self._user_dataset = self._user_dataset.append(self._process_user(user=user), ignore_index=True)

    def _process_user(self, user, n_tweets=20):

        """ Process a single user, collecting all the information """

        raw_data = [getattr(user, attr) for attr in _all_user_attributes]  # user attributes

        raw_data.append(utils.get_date())  # profile crawled
        raw_data.append(0)  # is suspended
        raw_data.append(n_tweets)  # number of collected tweets

        # TODO: add new attributes data related to its tweets
        tmp_tweets = self.collect_tweets(screen_name=user.screen_name, n_tweets=n_tweets)
        raw_data.append(tmp_tweets["length"].mean())  # mean length of tweets
        raw_data.append([id_ for id_ in tmp_tweets["quoted_user_id"]])  # quoted user ids

        raw_data = pd.Series(raw_data, index=self._user_dataset.columns)
        return raw_data[self._user_attrs_selectors]

    # TWEETS

    def collect_tweets(self, screen_name, n_tweets=20):

        """ Collect some tweets for a specific account, retrieving their attributes
        :param screen_name: screen_name of the account for which retrieve their tweets
        :param n_tweets: number of tweets to collect for that account
        :return: DataFrame containing all tweets collected for this user"""

        temporary_tweets_set = create_twitter_tweets_dataframe(self._tweets_attrs_selectors)
        for tweet in tweepy.Cursor(self._api.user_timeline, id=screen_name,  tweet_mode='extended').items(n_tweets):
            temporary_tweets_set = temporary_tweets_set.append(self._process_tweet(tweet=tweet), ignore_index=True)

        return temporary_tweets_set

    def _process_tweet(self, tweet):

        """ Process a single tweet
        :param tweet: tweet that has to be processed, by extracting all information
        :return: pandas Series containing all the information for that tweet"""

        raw_data = [getattr(tweet, attr) for attr in _all_tweets_attributes]

        raw_data.append(tweet.user.id)  # owner id
        raw_data.append(len(tweet.full_text))  # length of the text
        raw_data.append([ht["text"] for ht in tweet.entities["hashtags"]])  # hashtags
        raw_data.append([med["media_url_https"] for med in tweet.entities["media"]])  # media urls
        if tweet.is_quote_status:
            raw_data.append(tweet.quoted_status.user.id)  # original tweet's user id
        else:
            raw_data.append(None)

        raw_data = pd.Series(raw_data, index=self._tweets_dataset.columns)

        raw_data = raw_data[self._tweets_attrs_selectors]

        if self._collect_tweets:
            self._tweets_dataset = self._tweets_dataset.append(raw_data, ignore_index=True)
        return raw_data

    # TODO: collect data through json file

    # CSV CONVERTER

    def user_dataset_to_csv(self, filename, sep="\t"):
        self._user_dataset.to_csv(path_or_buf=filename, sep=sep, index=False)

    def tweets_dataset_to_csv(self, filename, sep=","):
        self._tweets_dataset.to_csv(path_or_buf=filename, sep=sep, index=False)