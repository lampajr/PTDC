# PTDC
# Copyright 2019 Lamparelli Andrea
# See LICENSE for details.

import logging

import tweepy

from ptdc import support
from ptdc.collector import Collector


class Streamer(tweepy.StreamListener):

    def __init__(self,
                 api,
                 time_limit=None,
                 data_limit=None,
                 json_path="../data/default_stream_file.json",
                 filter_user=lambda x: True,
                 filter_status=lambda x: True,
                 n_statuses=20,
                 verbose=True):

        """
        Streamer constructor, it represents an offline streamer, store streaming data into a file
        :param api: tweepy api
        :param time_limit: duration of the streaming, if None don't consider so it will last until process interrupt
        :param data_limit: number of data to collect at most (streaming data), if None don't consider
        :param json_path: file's location where saving the data collected, if None print on the std output
        :param filter_user: user filter function: User --> Bool
        :param filter_status: status filter function: Status --> Bool
        :param n_statuses: number of statuses to collect
        :param verbose: verbosity
        """

        super(Streamer, self).__init__()
        self.api = api
        self.time_limit = time_limit
        self.data_limit = data_limit
        self.json_path = json_path
        self.filter_user = filter_user
        self.filter_status = filter_status
        self.n_statuses = n_statuses
        self.start_time = 0
        self.count = 0
        self.file = None
        self.verbose = verbose

    def on_connect(self):

        """
        Called when the connection with
        the streaming server is established
        """

        logging.debug("connection with streaming server established!")

        self.start_time = support.get_time()
        self.count = 0

        logging.debug("Streaming started at {}".format(support.get_date()))

        if self.json_path is not None:
            # open or create a new file
            try:
                self.file = open(self.json_path, "a")
            except FileNotFoundError:
                self.file = open(self.json_path, "w")

    def on_data(self,
                raw_data):

        """ Called when new data is available """

        logging.debug("New data received..")

        # if enough time was passed stop streaming or enough data was collected
        if (self.time_limit is not None and (support.get_time() - self.start_time) > self.time_limit) \
                or (self.data_limit is not None and self.count >= self.data_limit):
            # if file has been opened, close it
            if self.file is not None:
                self.file.close()
                self.file = None

            logging.debug("Streaming terminated at {}".format(support.get_date()))
            logging.debug("Streaming duration = {} seconds".format(self.time_limit))

            # stop connection to w/ streaming server
            return False
        elif self.file is not None:
            # print the raw data on the file
            self.file.write(raw_data)
            self.file.write("\n")

        # call on_data of the superclass
        super(Streamer, self).on_data(raw_data=raw_data)

    def on_error(self, status_code):
        logging.error("Streaming error occurred: {}".format(status_code))

    def stream(self,
               follow=None,
               track=None,
               is_async=False,
               locations=None,
               stall_warnings=False,
               languages=None,
               encoding='utf8',
               filter_level=None):

        """
        Start the streaming in according to the filtering options passed as parameters
        For more detailed description of the parameters see Tweepy Stream class
        :param follow:
        :param track:
        :param is_async:
        :param locations:
        :param stall_warnings:
        :param languages:
        :param encoding:
        :param filter_level:
        """

        stream_ = tweepy.Stream(auth=self.api.auth, listener=self)
        stream_.filter(follow=follow, track=track, is_async=is_async, locations=locations,
                       stall_warnings=stall_warnings, languages=languages, encoding=encoding, filter_level=filter_level)


class OnlineStreamer(Streamer):

    """ Online Streamer that collects users and/or statuses during the streaming, e.g. online """

    def __init__(self,
                 api,
                 collector=None,
                 time_limit=None,
                 data_limit=None,
                 json_path="../data/default_stream_file.json",
                 filter_user=lambda x: True,
                 filter_status=lambda x: True,
                 verbose=True):

        super(OnlineStreamer, self).__init__(api=api,
                                             time_limit=time_limit,
                                             data_limit=data_limit,
                                             json_path=json_path,
                                             filter_user=filter_user,
                                             filter_status=filter_status,
                                             verbose=verbose)

        # collector needed for online data collection
        self.collector = Collector(api=self.api) if collector is None else collector

    def on_status(self, status):

        """ called when raw data is received from stream """

        self.collector.collect_user(screen_name=status.user.screen_name,
                                    filter_user=self.filter_user,
                                    filter_status=self.filter_status,
                                    n_statuses=self.n_statuses)

        self.count += 1


class OnlineStatusStreamer(Streamer):

    """ Online Streamer that collects statuses into DataFrame during streaming """

    def __init__(self,
                 api,
                 collector=None,
                 time_limit=None,
                 data_limit=None,
                 json_path="../data/default_stream_file.json",
                 filter_user=lambda x: True,
                 filter_status=lambda x: True,
                 verbose=True):

        super(OnlineStatusStreamer, self).__init__(api=api,
                                                   time_limit=time_limit,
                                                   data_limit=data_limit,
                                                   json_path=json_path,
                                                   filter_user=filter_user,
                                                   filter_status=filter_status,
                                                   verbose=verbose)

        # collector needed for online data collection
        self.collector = Collector(api=self.api) if collector is None else collector

    def on_status(self, status):

        """ called when raw data is received from stream """

        self.collector.collect_statuses(screen_name=status.user.screen_name,
                                        filter_status=self.filter_status,
                                        n_statuses=self.n_statuses)
        self.count += 1