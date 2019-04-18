import pandas as pd
import numpy as np
import tweepy

from ptdc import utils

def create_twitter_account_dataframe(attributes):

    """
    Create an empty pandas DataFrame with specified attributes, suitable for storing user's information
    :param attributes: Numpy array of attributes to be considered in the dataframe as columns
    """

    # create empty DataFrame with specified attributes
    _dataset = pd.DataFrame(columns=attributes)

    return _dataset


def create_twitter_statuses_dataframe(attributes):

    """
    Create an empty pandas DataFrame with specified attributes, suitable for storing status's information
    :param attributes: Numpy array of attributes to be considered in the dataframe as columns
    """

    # create empty DataFrame with specified attributes
    _dataset = pd.DataFrame(columns=attributes)

    return _dataset


class Collector(object):

    """ Data Collector that stores the DataFrames of the account and/or their tweets:
    provides methods for handling the data, adding new users, removing users.."""

    def __init__(self, api, collect_users=True, collect_tweets=True,
                 user_attr_dict=None, user_tweets_attr_dict=None, tweet_attr_dict=None,
                 verbose=True):
        """
        Data Collector constructor
        :param api: tweepy api used for querying
        :param collect_users: bool, tells whether or not collect users
        :param collect_tweets: bool, tells whether or not collect tweets
        :param user_attr_dict: dict <attribute, function> for user. func takes user and attribute name
        :param user_tweets_attr_dict: dict <attribute, function> for user. func takes user's tweets and attribute name
        :param tweet_attr_dict: dict <attribute, function> for tweet. function takes tweet and attribute name
        :param verbose: bool, verbosity
        """
        self.verbose = verbose
        self._collect_tweets = collect_tweets
        self._collect_users = collect_users

        self._user_attr_dict = utils.default_user_dict if user_attr_dict is None else user_attr_dict
        self._user_tweets_attr_dict = utils.default_user_tweets_dict if user_tweets_attr_dict is None else user_tweets_attr_dict
        self._tweet_attr_dict = utils.default_tweet_dict if tweet_attr_dict is None else tweet_attr_dict

        # empty datasets
        self._user_dataset = create_twitter_account_dataframe(attributes=np.array(np.concatenate((
            np.array(list(self._user_attr_dict.keys())), np.array(list(self._user_tweets_attr_dict.keys()))))))
        self._tweets_dataset = create_twitter_statuses_dataframe(attributes=np.array(list(self._tweet_attr_dict.keys())))

        # Twitter api for making query
        self._api = api

    def get_users_dataset(self):

        """
        :returns: pandas DataFrame containing collected accounts
        """

        return self._user_dataset

    def get_tweets_dataset(self):

        """
        :returns: pandas DataFrame containing collected tweets
        """

        return self._tweets_dataset

    # USERS

    def collect_user(self, screen_name, n_tweets=utils.DEFAULT_N_TWEETS):

        """
        Collect all the information about a specific Account
        :param screen_name: the screen_name/id of the account
        :param n_tweets: number of tweets to collect for this user
        """

        user = self._api.get_user(screen_name)

        if self.verbose:
            print("Collecting user {}".format(screen_name))

        self._user_dataset = self._user_dataset.append(self._process_user(user=user, n_tweets=n_tweets), ignore_index=True)

        if self.verbose:
            print("User collected!")

    def _process_user(self, user, n_tweets):

        """
        Process a single user, collecting all the information
        :param user: Twitter user object
        :param n_tweets: number of tweets to collect for this user
        :return: raw_data containing all attributes' values for this user
        """

        user_data = [func(user, attr_name) for attr_name, func in self._user_attr_dict.items()]  # user's attributes

        # collect user's tweets
        tmp_tweets = self.collect_statuses(screen_name=user.screen_name, n_tweets=n_tweets)

        user_tweets_data = [func(tmp_tweets, attr_name) for attr_name, func in self._user_tweets_attr_dict.items()]

        raw_data = pd.Series(user_data+user_tweets_data, index=self._user_dataset.columns)
        return raw_data

    # TWEETS

    def collect_statuses(self, screen_name, n_tweets=utils.DEFAULT_N_TWEETS):

        """
        Collect some tweets for a specific account, retrieving their attributes
        :param screen_name: screen_name of the account for which retrieve their tweets
        :param n_tweets: number of tweets to collect for that account
        :return: DataFrame containing all tweets collected for this user"""

        tmp_statuses_set = create_twitter_statuses_dataframe(np.array(list(self._tweet_attr_dict.keys())))
        for status in tweepy.Cursor(self._api.user_timeline, id=screen_name,  tweet_mode='extended').items(n_tweets):
            tmp_statuses_set = tmp_statuses_set.append(self._process_status(status=status), ignore_index=True)

        return tmp_statuses_set

    def _process_status(self, status):

        """ Process a single tweet
        :param status: Twitter tweet object that has to be processed, by extracting all its information
        :return: pandas Series containing all the information for that tweet: raw_data """

        tweet_data = [func(status, attr_name) for attr_name, func in self._tweet_attr_dict.items()]  # tweet's attributes

        raw_data = pd.Series(tweet_data, index=self._tweets_dataset.columns)

        if self._collect_tweets:
            self._tweets_dataset = self._tweets_dataset.append(raw_data, ignore_index=True)

        return raw_data

    # TODO: collect data through json file

    #################################################
    ################# CSV CONVERTER #################
    #################################################

    def user_dataset_to_csv(self, filename, sep="\t"):
        if self.verbose:
            print("Saving users dataset at {}".format(filename))
        self._user_dataset.to_csv(path_or_buf=filename, sep=sep, index=False)

    def tweets_dataset_to_csv(self, filename, sep="\t"):
        if self.verbose:
            print("Saving tweets dataset at {}".format(filename))
        self._tweets_dataset.to_csv(path_or_buf=filename, sep=sep, index=False)