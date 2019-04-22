"""
Streamer module, it contains all Streamer object used for listening on Twitter channel
Streamer -> makes an offline collection, since it simply print data listened in json format
OnlineStreamer -> beyond printing streamed data, it will collect users and/or statuses directly during streaming,
                  it requires a Collector obj
OnlineStatusesStreamer -> it collects data during streaming, but in this case only statuses are collected.


:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""

import logging
import time

from urllib3.exceptions import ProtocolError

import tweepy

from ptdc import support
from ptdc.collector import Collector


class Streamer(tweepy.StreamListener):

    def __init__(self,
                 apis,
                 time_limit=None,
                 data_limit=None,
                 json_path="../data/default_stream_file.json",
                 filter_user=lambda x: True,
                 filter_status=lambda x: True,
                 n_statuses=20,
                 attempts=None,
                 backup=None,
                 verbose=True):

        """
        Streamer constructor, it represents an offline streamer, store streaming data into a file
        :param apis: list of tweepy APIs
        :param time_limit: duration of the streaming, if None don't consider so it will last until process interrupt
        :param data_limit: number of data to collect at most (streaming data), if None don't consider
        :param json_path: file's location where saving the data collected, if None print on the std output
        :param filter_user: user filter function: User --> Bool
        :param filter_status: status filter function: Status --> Bool
        :param n_statuses: number of statuses to collect
        :param attempts: number of reconnection attempts to perform in case of streaming failure, first connection
                         excluded, if None always retry to reconnect
        :param backup: every how many seconds to backup, if None no backup is scheduled
        :param verbose: verbosity
        """

        super(Streamer, self).__init__()
        self.apis = apis
        self._idx = 0
        self.time_limit = time_limit
        self.data_limit = data_limit
        self.json_path = json_path
        self.filter_user = filter_user
        self.filter_status = filter_status
        self.n_statuses = n_statuses
        self.attempts = attempts
        self.backup = backup
        self.verbose = verbose

        self.start_time = 0
        self.last_backup = 0
        self.count = 0
        self.file = None
        self._closed = False

    def on_connect(self):

        """
        Called when the connection with
        the streaming server is established
        """

        logging.debug("connection with streaming server established!")

        self.start_time = support.get_time()
        self.last_backup = self.start_time
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

            self._closed = True
            # stop connection to w/ streaming server
            return False
        elif self.file is not None:
            # print the raw data on the file
            self.file.write(raw_data)
            self.file.write("\n")

        # call on_data of the superclass
        super(Streamer, self).on_data(raw_data=raw_data)

    def on_error(self, status_code):

        """Called when a non-200 status code is returned"""

        logging.warning("status code={}".format(status_code))
        if status_code == 401:
            # UNAUTHORIZED
            raise tweepy.TweepError(reason="Missing or incorrect authentication credentials", api_code=status_code)
        elif status_code == 88:
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
                stream_ = tweepy.Stream(auth=self.apis[self._idx].auth, listener=self)
                stream_.filter(follow=follow, track=track, is_async=is_async, locations=locations,
                               stall_warnings=stall_warnings, languages=languages, encoding=encoding,
                               filter_level=filter_level)
            except tweepy.RateLimitError as e:
                # change API, if any and try to restart streaming
                logging.warning(e)
                logging.warning("Changing API..")
                self._idx = (self._idx + 1) % len(self.apis)
                continue
            except (ProtocolError, tweepy.TweepError) as e:
                logging.warning(e)
                logging.warning("Reconnecting...")
                # sleep for 5 seconds
                self.attempts -= 1
                continue

        if self.attempts is not None and self.attempts == 0 and not self._closed:
            logging.error("Limit number of attempts reached!!")


class OnlineStreamer(Streamer):

    """ Online Streamer that collects users and/or statuses during the streaming, e.g. online """

    def __init__(self,
                 apis,
                 collector=None,
                 time_limit=None,
                 data_limit=None,
                 json_path="../data/default_stream_file.json",
                 filter_user=lambda x: True,
                 filter_status=lambda x: True,
                 n_statuses=20,
                 attempts=0,
                 backup=None,
                 verbose=True):

        super(OnlineStreamer, self).__init__(apis=apis,
                                             time_limit=time_limit,
                                             data_limit=data_limit,
                                             json_path=json_path,
                                             filter_user=filter_user,
                                             filter_status=filter_status,
                                             n_statuses=n_statuses,
                                             attempts=attempts,
                                             backup=backup,
                                             verbose=verbose)

        # collector needed for online data collection
        self.collector = Collector(apis=self.apis) if collector is None else collector

    def on_status(self, status):

        """ called when raw data is received from stream """

        if self.check_backup():
            self.last_backup = support.get_time()
            self.collector.backup()

        self.collector.collect_user(screen_name=status.user.screen_name,
                                    filter_user=self.filter_user,
                                    filter_status=self.filter_status,
                                    n_statuses=self.n_statuses)

        self.count += 1


class OnlineStatusStreamer(Streamer):

    """ Online Streamer that collects statuses into DataFrame during streaming """

    def __init__(self,
                 apis,
                 collector=None,
                 time_limit=None,
                 data_limit=None,
                 json_path="../data/default_stream_file.json",
                 filter_user=lambda x: True,
                 filter_status=lambda x: True,
                 n_statuses=20,
                 attempts=0,
                 backup=None,
                 verbose=True):

        super(OnlineStatusStreamer, self).__init__(apis=apis,
                                                   time_limit=time_limit,
                                                   data_limit=data_limit,
                                                   json_path=json_path,
                                                   filter_user=filter_user,
                                                   filter_status=filter_status,
                                                   n_statuses=n_statuses,
                                                   attempts=attempts,
                                                   backup=backup,
                                                   verbose=verbose)

        # collector needed for online data collection
        self.collector = Collector(apis=self.apis, collect_users=False) if collector is None else collector

    def on_status(self, status):

        """ called when raw data is received from stream """

        if self.check_backup():
            self.last_backup = support.get_time()
            self.collector.backup()

        self.collector.collect_statuses(screen_name=status.user.screen_name,
                                        filter_status=self.filter_status,
                                        n_statuses=self.n_statuses)
        self.count += 1