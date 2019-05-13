"""
Collector module, it contains the Collector class that represents tha main
point used for storing data collected from twitter.
the collector will make queries to Twitter, through Tweepy API, and stores
the data into Pandas DataFrame.

:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""

import logging
from abc import ABC, abstractmethod
from functools import reduce

import numpy as np
import pandas as pd
import tweepy

from ptdc.support import get_attribute, get_retweeted_user_id, get_retweeted_status, get_quoted_user_id, get_media, \
    get_date, get_country, get_place_type

default_account_features = {"id": get_attribute,
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
                            "following_followers_ratio": lambda user, _: user.friends_count / user.followers_count if user.followers_count != 0 else None,
                            "followers_following_ratio": lambda user, _: user.followers_count / user.friends_count if user.friends_count != 0 else None}


default_account_timeline_features = {"n_statuses_collected": lambda statuses_data, _: statuses_data.shape[0],
                                     "mean_status_length": lambda statuses_data, _: statuses_data["text_length"].mean(),
                                     "media_shared_urls": lambda statuses_data, _: reduce(lambda x,y: x+y, [], [x for x in statuses_data["media_urls"] if x is not None]),
                                     "mean_shared_media": lambda statuses_data, _: (len(reduce(lambda x,y: x+y, [], [x for x in statuses_data["media_urls"] if x is not None])) / statuses_data.shape[0]) if statuses_data.shape[0] != 0 else None,
                                     "quoted_user_ids": lambda statuses_data, _: [x for x in statuses_data["quoted_user_id"] if x is not None],
                                     "replied_status_ids": lambda statuses_data, _: [x for x in statuses_data["in_reply_to_status_id"] if x is not None],
                                     "replied_user_ids": lambda statuses_data, _: [x for x in statuses_data["in_reply_to_user_id"] if x is not None],
                                     "retweeted_status_ids": lambda statuses_data, _: [x for x in statuses_data["retweeted_status"] if x is not None],
                                     "retweeted_user_ids": lambda statuses_data, _: [x for x in statuses_data["retweeted_user_id"] if x is not None]}


default_statuses_features = {"id": get_attribute,
                             "created_at": get_attribute,
                             "full_text": get_attribute,
                             "lang": get_attribute,
                             "coordinates": get_attribute,
                             "retweet_count": get_attribute,
                             "favorite_count": get_attribute,
                             "source": get_attribute,
                             "truncated": get_attribute,
                             "is_quote_status": get_attribute,
                             "in_reply_to_status_id": get_attribute,
                             "in_reply_to_user_id": get_attribute,
                             "in_reply_to_screen_name": get_attribute,
                             "user_id": lambda status, _: status.user.id,
                             "text_length": lambda status, _: len(status.full_text),
                             "hashtags": lambda status, feature: [ht["text"] for ht in status.entities[feature]],
                             "user_mentions": lambda status, feature: [user["screen_name"] for user in status.entities[feature]],
                             "symbols": lambda status, feature: status.entities[feature],
                             "media_urls": lambda status, _: get_media(status),
                             "quoted_user_id": lambda status, _: get_quoted_user_id(status),
                             "retweeted_status": lambda status, _: get_retweeted_status(status),
                             "retweeted_user_id": lambda status, _: get_retweeted_user_id(status),
                             "country": lambda status, _: get_country(status),
                             "place_type": lambda status, _: get_place_type(status)}


class Collector(ABC):

    """ Abstract Data Collector """

    MAX_STATUSES = 3200  # maximum number of statuses that can be collected from a single account

    def __init__(self, api, verbose=True):
        super(Collector, self).__init__()
        self.api = api
        self._verbose = verbose
        self._dataset = None
        self.count = 0
        self.verboseprint = print if self._verbose else lambda *args: None

    def dataset(self):
        return self._dataset

    @abstractmethod
    def process(self,
                screen_name,
                n_statuses,
                filter_account=lambda x: True,
                filter_status=lambda x: True):

        """
        Method called by the OnlineStreamer used for collecting data online,
        Must be implemented by all sub-classes collector, each of one will define their own
        collection procedure
        :param screen_name: screen_name of the user streamed
        :param n_statuses: number of statuses to be collected for that user
        :param filter_account: filtering function for users
        :param filter_status: filtering function for statuses
        """
        pass

    def init_dataset(self, features):

        """
        Create the empty dataframe
        :param features: features  numpy array
        """

        logging.debug("Initializing DataFrame..")

        self._dataset = pd.DataFrame(columns=features)

    def update_dataset(self, data):

        """
        Update the current dataset with new raw_data
        :param data: pandas Series data to add in the df
        """

        self._dataset = self._dataset.append(data, ignore_index=True)

    def save_dataset(self, path, sep='\t'):
        """
        Save the dataset at given location
        :param path: path where save the dataset
        :param sep: separator used, default '\t'
        """

        self._dataset.to_csv(path_or_buf=path, sep=sep, index=False)

        self.verboseprint("Dataset successfully saved at {}.".format(path))
        logging.debug("Dataset saved at {}..".format(path))


class AccountCollector(Collector):

    """ Twitter's Accounts Data Collector """

    def __init__(self,
                 api,
                 statuses_collector=None,
                 features=None,
                 timeline_features=None,
                 verbose=True):

        """
        Account Collector constructor
        :param api: Tweepy API obj used for making query
        :param statuses_collector: StatusCollector used for storing statuses
        :param features: account features dict -> <feature_name, func>, func takes user and feature name
        :param timeline_features: features related to the account timeline, dict <feature_name, func>,
                                  func takes timeline dataframe and feature name
        """

        super(AccountCollector, self).__init__(api=api, verbose=verbose)

        self._features = default_account_features if features is None else features
        self._timeline_features = default_account_timeline_features if timeline_features is None else timeline_features

        self._all_features = np.array(np.concatenate((np.array(list(self._features.keys())), np.array(list(self._timeline_features.keys())))))

        self._statuses_collector = statuses_collector

        self.init_dataset(self._all_features)

    def save_dataset(self, path, sep='\t'):

        """
        Override of parent's class method, allowing user to saves also statuses collected,
        if statuses_collector is not None
        :param path: Accounts file's path
        :param sep: separator of csv
        """

        if self._statuses_collector is not None:
            statuses_path = path[:path.rfind(".")] + "_statuses.csv"
            self._statuses_collector.save_dataset(path=statuses_path, sep=sep)
        super(AccountCollector, self).save_dataset(path=path, sep=sep)

    def process(self,
                screen_name,
                n_statuses,
                filter_account=lambda x: True,
                filter_status=lambda x: True):

        """ Overrided method, see super class doc"""

        self.collect_account(screen_name=screen_name,
                             n_statuses=n_statuses,
                             filter_account=filter_account,
                             filter_status=filter_status)

    def collect_account(self,
                        screen_name,
                        n_statuses,
                        filter_account=lambda x: True,
                        filter_status=lambda x: True):
        """
        Method that collects account's information
        :param screen_name: screen_name or id of the account to retrieve
        :param n_statuses: number of account's statuses to collect
        :param filter_account: filtering function to apply to the Account obj
        :param filter_status: filtering function to apply to the Status obj
        """
        self.verboseprint("Collecting account.", end='\r')
        logging.debug("Collecting account infos..")
        account = self.api.get_user(screen_name)
        if filter_account(account):
            self.update_dataset(data=self._process_account(account=account,
                                                           n_statuses=n_statuses,
                                                           filter_status=filter_status))
        else:
            self.verboseprint("Account skipped..")
            logging.debug("Account skipped..")
        self.count += 1

        if (self.count % 20) == 0:
            self.verboseprint("Collected {} accounts!".format(self.count))

    def _process_account(self, account, n_statuses, filter_status):

        """
        Retrieve all pre-defined features for the given account
        :param account: account for which get info
        :param n_statuses: number of statuses to collect for this account
        :return: pandas Series containing all information
        """

        account_data = [func(account, feature_name) for feature_name, func in self._features.items()]
        if self._timeline_features:
            # creates a local default collector for retrieving timeline features
            local_collector = self._statuses_collector if self._statuses_collector is not None else StatusCollector(api=self.api)
            status_df = local_collector.collect_statuses(screen_name=account.screen_name, n_statuses=n_statuses, filter_status=filter_status)
            status_data = [func(status_df, feature_name) for feature_name, func in self._timeline_features.items()]
            account_data = account_data + status_data

        raw_data = pd.Series(account_data, index=self.dataset().columns)
        return raw_data


class StatusCollector(Collector):

    """ Twitter's Statuses Data Collector """

    def __init__(self,
                 api,
                 features=None,
                 verbose=True):
        super(StatusCollector, self).__init__(api=api, verbose=verbose)

        self._features = default_statuses_features if features is None else features
        self._all_features = np.array(list(self._features.keys()))

        self.init_dataset(features=self._all_features)

    def process(self,
                screen_name,
                n_statuses,
                filter_account=lambda x: True,
                filter_status=lambda x: True):

        """ Overrided method, see super class doc"""

        self.collect_statuses(screen_name=screen_name,
                              n_statuses=n_statuses,
                              filter_status=filter_status)

    def collect_statuses(self, screen_name, n_statuses, filter_status=lambda x: True):

        """
        Collect statuses from a specific account's timeline
        :param screen_name: screen name or id of the account
        :param n_statuses: number of statuses to collect for thus account
        :param filter_status: filtering function to apply to Status obj
        :return local DataFrame containing the statuses of this account
        """

        n_statuses = Collector.MAX_STATUSES if n_statuses > Collector.MAX_STATUSES else n_statuses

        # hold all account's statuses
        all_statuses = []

        count = 200 if n_statuses > 200 else n_statuses
        new_statuses = self.api.user_timeline(screen_name=screen_name, tweet_mode='extended', count=count)

        # save the most recent statuses
        all_statuses.extend(new_statuses)

        self.verboseprint("Collecting account", end='')

        # save the id of the oldest status

        oldest = all_statuses[-1].id if len(all_statuses) > 0 else None

        # keep grabbing statuses until no statuses left to grab or the total amount of statuses to collect was reached
        while len(new_statuses) > 0 and len(all_statuses) < n_statuses:
            try:
                # remaining statuses to collect
                remaining_statuses = n_statuses - len(all_statuses)
                count = 200 if remaining_statuses > 200 else remaining_statuses

                # collect oldest statuses wrt previous query
                new_statuses = self.api.user_timeline(screen_name=screen_name, tweet_mode='extended', count=count, max_id=oldest)
                all_statuses.extend(new_statuses)

                # update oldest status
                oldest = all_statuses[-1].id - 1

                self.verboseprint(".", end='')
                logging.debug("Collected {}/{} statuses..".format(len(all_statuses), n_statuses))
            except tweepy.TweepError as e:
                logging.warning(e)
                continue

        self.verboseprint("\nAccount collected : {}/{} statuses..".format(len(all_statuses), n_statuses))
        logging.debug("Collected {}/{} statuses..".format(len(all_statuses), n_statuses))

        all_statuses = np.array(all_statuses)
        # keep all statuses that satisfy the filtering function
        all_statuses = all_statuses[list(map(filter_status, all_statuses))]

        local_df = pd.DataFrame(columns=self._all_features)
        for st in all_statuses:
            raw_data = self._process_status(st)
            local_df = local_df.append(raw_data, ignore_index=True)

        self.update_dataset(data=local_df)

        return local_df

    def _process_status(self, status):

        """
        Process a single status retrieving all the pre-defined information
        :param status: status obj
        :return: pandas Series containing all the infos
        """

        return pd.Series([func(status, attr_name) for attr_name, func in self._features.items()], index=self.dataset().columns)

