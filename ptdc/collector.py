"""
Collector module, it contains the Collector class that represents tha main
point used for storing data collected from twitter.
the collector will make queries to Twitter, through Tweepy API, and stores
the data into Pandas DataFrame.

:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""

import json
import logging

import numpy as np
import pandas as pd
import tweepy

from ptdc import data as dd


class Collector(object):

    """ Data Collector that stores the DataFrames of the account and/or their tweets:
    provides methods for handling the data, adding new users, removing users.."""

    def __init__(self,
                 api,
                 collect_users=True,
                 collect_statuses=True,
                 user_attr_dict=None,
                 user_tweets_attr_dict=None,
                 tweet_attr_dict=None,
                 verbose=True):
        """
        Data Collector constructor
        :param api: tweepy api used for querying Twitter
        :param collect_users: bool, tells whether or not collect users
        :param collect_statuses: bool, tells whether or not collect statuses
        :param user_attr_dict: dict <attribute, func> for user. func takes user and attribute name
        :param user_tweets_attr_dict: dict <attribute, func> for user. func takes tweets dataframe and attribute name
        :param tweet_attr_dict: dict <attribute, func> for tweet. function takes tweet and attribute name
        :param verbose: bool, verbosity
        """
        self.verbose = verbose
        self._collect_statuses = collect_statuses
        self._collect_users = collect_users

        self._user_attr_dict = dd.default_user_dict if user_attr_dict is None else user_attr_dict
        self._user_statuses_attr_dict = dd.default_user_tweets_dict if user_tweets_attr_dict is None \
            else user_tweets_attr_dict
        self._tweet_attr_dict = dd.default_tweet_dict if tweet_attr_dict is None else tweet_attr_dict

        # empty datasets
        self._users_dataset = pd.DataFrame(columns=np.array(np.concatenate((
            np.array(list(self._user_attr_dict.keys())), np.array(list(self._user_statuses_attr_dict.keys()))))))
        self._statuses_dataset = pd.DataFrame(columns=np.array(list(self._tweet_attr_dict.keys())))

        # Twitter api for making query
        self._api = api

    def get_users_dataset(self):

        """
        :returns: pandas DataFrame containing collected accounts
        """

        return self._users_dataset

    def get_tweets_dataset(self):

        """
        :returns: pandas DataFrame containing collected tweets
        """

        return self._statuses_dataset

    ###########################################
    ############ COLLECTOR METHODS ############
    ###########################################

    def collect_user(self,
                     screen_name,
                     filter_user=lambda x: True,
                     filter_status=lambda x: True,
                     n_statuses=20):

        """
        Collect all the information about a specific Account
        :param screen_name: the screen_name/id of the account
        :param filter_user: filtering function that takes as input the user obj and return True or False
                        indicating whether collect the user or not
        :param filter_status: filtering function that takes as input the status obj and return True or False
                        indicating whether collect the tweet or not
        :param n_statuses: number of statuses to collect for this user
        """

        user = self._api.get_user(screen_name)

        if filter_user(user):
            logging.debug("Collecting user {}".format(screen_name))

            self._users_dataset = self._users_dataset.append(self._process_user(user=user,
                                                                                filter_status=filter_status,
                                                                                n_statuses=n_statuses),
                                                             ignore_index=True)

            logging.debug("User collected!")
        else:
            logging.debug("User skipped..")

    def _process_user(self,
                      user,
                      filter_status,
                      n_statuses):

        """
        Process a single user, collecting all the information
        :param user: Twitter user object
        :param filter_status: status filter function, collect status or not
        :param n_statuses: number of statuses to collect for this user
        :return: raw_data containing all attributes' values for this user
        """

        user_data = [func(user, attr_name) for attr_name, func in self._user_attr_dict.items()]  # user's attributes

        if self._user_statuses_attr_dict or self._collect_statuses:
            # collect user's statuses if the dict is not empty
            tmp_tweets = self.collect_statuses(screen_name=user.screen_name,
                                               filter_status=filter_status,
                                               n_statuses=n_statuses)
            if self._user_statuses_attr_dict:
                user_statuses_data = [func(tmp_tweets, attr_name) for attr_name, func in
                                      self._user_statuses_attr_dict.items()]
                user_data = user_data + user_statuses_data

        raw_data = pd.Series(user_data, index=self._users_dataset.columns)
        return raw_data

    def collect_statuses(self,
                         screen_name,
                         filter_status=lambda x: True,
                         n_statuses=20):

        """
        Collect some tweets for a specific account, retrieving their attributes
        :param screen_name: screen_name of the account for which retrieve their tweets
        :param filter_status: filtering function that takes as input the status obj and return True or False
                        indicating whether collect the tweet or not
        :param n_statuses: number of tweets to collect for that account
        :return: DataFrame containing all tweets collected for this user"""

        tmp_statuses_set = pd.DataFrame(columns=np.array(list(self._tweet_attr_dict.keys())))
        for status in tweepy.Cursor(self._api.user_timeline, id=screen_name,  tweet_mode='extended').items(n_statuses):
            if filter_status(status):
                tmp_statuses_set = tmp_statuses_set.append(self._process_status(status=status), ignore_index=True)

        return tmp_statuses_set

    def _process_status(self,
                        status):

        """
        Process a single status
        :param status: Twitter status object that has to be processed, by extracting all its information
        :return: pandas Series containing all the information for that tweet: raw_data """

        # status' attributes
        status_data = [func(status, attr_name) for attr_name, func in self._tweet_attr_dict.items()]

        raw_data = pd.Series(status_data, index=self._statuses_dataset.columns)

        if self._collect_statuses:
            self._statuses_dataset = self._statuses_dataset.append(raw_data, ignore_index=True)

        return raw_data

    def collect_from_json(self,
                          json_path,
                          filter_user=lambda x: True,
                          filter_status=lambda x: True,
                          n_statuses=20):

        """
        Collects data (users and/or statuses) from a json file
        :param json_path: path to the json file
        :param filter_user: user filter function, tells whether collect user or not
        :param filter_status: status filter function, tells whether collect status or not
        :param n_statuses: number of statuses to collect for each user
        """

        try:
            with open(json_path) as file:
                for line in file:
                    status = json.loads(line)
                    self.collect_user(screen_name=status["user"]["screen_name"],
                                      filter_user=filter_user,
                                      filter_status=filter_status,
                                      n_statuses=n_statuses)
        except FileNotFoundError:
            logging.warning("Json file not found.. make sure that the path is a valid one!")

    def collect_statuses_from_json(self,
                                   json_path,
                                   filter_status=lambda x: True,
                                   n_statuses=20):
        """
        Collects statuses from a json file
        :param json_path: path to the json file
        :param filter_status: status filter function, tells whether collect status or not
        :param n_statuses: number of statuses to collect for each user
        """

        try:
            with open(json_path) as file:
                for line in file:
                    status = json.loads(line)
                    self.collect_statuses(screen_name=status["user"]["screen_name"],
                                          filter_status=filter_status,
                                          n_statuses=n_statuses)
        except FileNotFoundError:
            logging.warning("Json file not found.. make sure that the path is a valid one!")

    #################################################
    ################# CSV CONVERTER #################
    #################################################

    def user_dataset_to_csv(self,
                            filename,
                            sep="\t"):
        logging.debug("Saving users dataset at {}".format(filename))
        self._users_dataset.to_csv(path_or_buf=filename, sep=sep, index=False)

    def tweets_dataset_to_csv(self,
                              filename,
                              sep="\t"):
        logging.debug("Saving tweets dataset at {}".format(filename))
        self._statuses_dataset.to_csv(path_or_buf=filename, sep=sep, index=False)
