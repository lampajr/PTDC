"""
Streamer module, it contains Streamer class used for listening on Twitter channel
OnlineStreamer -> makes an online collection, printing the streamed ata into a json file and directly collecting
                  all data through the usage of a specific collector.
                  @see Collector

:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""

import logging
import socket

import tweepy
from urllib3 import exceptions

from ptdc import support


class OnlineStreamer(tweepy.StreamListener):

    def __init__(self,
                 api,
                 collector,
                 n_statuses,
                 time_limit=None,
                 data_limit=None,
                 json_path="./streaming.json",
                 backup_path=None,
                 filter_user=lambda x: True,
                 filter_status=lambda x: True,
                 attempts=None,
                 backup=None,
                 verbose=True):

        """
        Streamer constructor, it represents an offline streamer, store streaming data into a file
        :param api: tweepy API obj
        :param collector, Collector obj used for collecting data streamed
        :param n_statuses: number of statuses to collect
        :param time_limit: duration of the streaming, if None don't consider so it will last until process interrupt
        :param data_limit: number of data to collect at most (streaming data), if None don't consider
        :param json_path: file's location where saving the data collected, if None print on the std output
        :param backup_path: backup file's path
        :param filter_user: user filter function: User --> Bool
        :param filter_status: status filter function: Status --> Bool
        :param attempts: number of reconnection attempts to perform in case of streaming failure, first connection
                         excluded, if None always retry to reconnect
        :param backup: every how many seconds to backup, if None no backup is scheduled
        :param verbose: verbosity
        """

        super(OnlineStreamer, self).__init__()
        self.api = api
        self.time_limit = time_limit
        self.data_limit = data_limit
        self.json_path = json_path
        self.backup_path = backup_path if backup_path is not None else "./.backup{}".format(support.get_time())
        self.filter_user = filter_user
        self.filter_status = filter_status
        self.n_statuses = n_statuses
        self.attempts = attempts
        self.backup = backup
        self._verbose = verbose
        # verbosity function
        self.verboseprint = print if self._verbose else lambda *args: None

        # collector needed for online data collection
        self.collector = collector

        self.start_time = 0
        self.last_backup = 0
        self.count = 0
        self.start_time = support.get_time()
        self.last_backup = self.start_time
        self.file = None
        self._closed = False

    def on_connect(self):

        """
        Called when the connection with
        the streaming server is established
        """

        self.verboseprint("Connection with streaming server established!")
        logging.debug("Connection with streaming server established!")

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
        if self._closed:
            # if file has been opened, close it
            if self.file is not None:
                self.file.close()
                self.file = None

            duration = self.time_limit if self.time_limit is not None else support.get_time() - self.start_time

            self.verboseprint("Streaming duration = {} seconds".format(duration))
            logging.debug("Streaming terminated at {}".format(support.get_date()))
            logging.debug("Streaming duration = {} seconds".format(duration))

            # stop connection to w/ streaming server
            return False
        elif self.file is not None:
            # print the raw data on the file
            self.file.write(raw_data)
            self.file.write("\n")

        # call on_data of the superclass
        super(OnlineStreamer, self).on_data(raw_data=raw_data)

    def on_status(self, status):

        """ called when raw data is received from stream """

        if self.check_backup():
            self.last_backup = support.get_time()
            self.collector.save_dataset(path=self.backup_path)

        self.collector.process(screen_name=status.user.screen_name,
                               filter_account=self.filter_user,
                               filter_status=self.filter_status,
                               n_statuses=self.n_statuses)

        self.count += 1
        if (self.data_limit is not None and self.count > self.data_limit) or \
                (self.time_limit is not None and (support.get_time() - self.start_time) > self.time_limit):
            self._closed = True

    def on_error(self, status_code):

        """Called when a non-200 status code is returned"""

        logging.warning("status code={}".format(status_code))
        if status_code == 401:
            # UNAUTHORIZED
            raise tweepy.TweepError(reason="Missing or incorrect authentication credentials", api_code=status_code)
        elif status_code == 420:
            # RATE LIMIT
            raise tweepy.RateLimitError(reason="The request limit for this resource has been reached")
        else:
            raise tweepy.TweepError("Unhandled exception: {}".format(status_code), api_code=status_code)

    def on_exception(self, exception):

        """Called when an unhandled exception occurs."""

        pass

    def check_backup(self):

        """ Checks whether is time to backup data """

        return self.backup is not None and (support.get_time() - self.last_backup) > self.backup

    def stream(self,
               follow=None,
               track=None,
               is_async=False,
               locations=None,
               stall_warnings=True,
               languages=None,
               encoding='utf8',
               filter_level=None):

        """
        Start the streaming in according to the filtering options passed as parameters
        :params follow, track, is_async, locations, stall_warnings, languages,
               encoding, filter_level: for more details about the parameters see Tweepy Stream class
        """

        while (self.attempts is None or self.attempts > 0) and not self._closed:
            try:
                stream_ = tweepy.Stream(auth=self.api.auth, listener=self)
                stream_.filter(follow=follow, track=track, is_async=is_async, locations=locations,
                               stall_warnings=stall_warnings, languages=languages, encoding=encoding,
                               filter_level=filter_level)
            except (socket.timeout, exceptions.ReadTimeoutError, exceptions.ProtocolError, tweepy.TweepError) as e:
                logging.warning(e)
                self.verboseprint("Reconnecting...")
                if self.attempts is not None:
                    self.attempts -= 1
                continue

        if self.attempts is not None and self.attempts == 0 and not self._closed:
            logging.error("Limit number of attempts reached!!")

