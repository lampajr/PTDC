import tweepy
import logging

from ptdc import utils
from ptdc.data import DataCollector


class Streamer(tweepy.StreamListener):

    def __init__(self, api, collector=None,  time_limit=None, path="../data/default_stream_file.json"):

        """ Streamer constructor, it represents an offline streamer, store streaming data into a file
         :param api: tweepy api
         :param time_limit: duration of the streaming, if None last forever
         :param path: file's location where saving the data collected, if None print on the std output """

        super(Streamer, self).__init__()
        self.api = api
        self.time_limit = time_limit
        self.path = path
        self.start_time = 0
        self.file = None
        self.collector = DataCollector(api=self.api) if collector is None else collector

    def on_connect(self):

        """ called when the connection with
        the streaming server is established """

        self.start_time = utils.get_time()
        logging.debug("Streaming started at {}".format(utils.get_date()))

        if self.path is not None:
            # open or create a new file
            try:
                self.file = open(self.path, "a")
            except FileNotFoundError:
                self.file = open(self.path, "w")

    def on_data(self, raw_data):

        """ Called when new data is available """

        # if enough time is passed stop streaming
        if self.time_limit is not None and (utils.get_time() - self.start_time) > self.time_limit:
            # if file has been opened, close it
            if self.file is not None:
                self.file.close()
                self.file = None
            # stop connection to he streaming server
            logging.debug("Streaming terminated at {}".format(utils.get_date()))
            logging.debug("Streaming duration = {} seconds".format(self.time_limit))
            return False
        elif self.file is not None:
            # print the raw data on the file
            self.file.write(raw_data)
            self.file.write("\n")

        # call on_data of the superclass
        super(Streamer, self).on_data(raw_data=raw_data)

    def on_error(self, status_code):
        print(status_code)

    def stream(self, follow=None, track=None, is_async=False, locations=None,
               stall_warnings=False, languages=None, encoding='utf8', filter_level=None):

        """ start the streaming in according to the filtering options passed as parameters """

        stream_ = tweepy.Stream(auth=self.api.auth, listener=self)
        stream_.filter(follow=follow, track=track, is_async=is_async, locations=locations,
                       stall_warnings=stall_warnings, languages=languages, encoding=encoding, filter_level=filter_level)


class OnlineStreamer(Streamer):

    """ Subclass of Streamer that collects data during the streaming, generating the corresponding DataFrame/s"""

    def __init__(self, api, time_limit=None, path="../data/default_stream_file.json"):

        """ Online streamer, collects data online during streaming
        w/o saving it into a specific text file """

        super(OnlineStreamer, self).__init__(api=api, time_limit=time_limit, path=path)

    def on_status(self, status):

        """ called when raw data is received from stream """

        self.collector.collect_user(screen_name=status.user.screen_name)