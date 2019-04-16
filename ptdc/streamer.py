import tweepy
import json
from abc import ABC, abstractmethod
from ptdc import utils


class Streamer(ABC, tweepy.StreamListener):

    def __init__(self, api,  time_limit=None, path=None):
        """ Streamer constructor
         :param api: tweepy api
         :param time_limit: duration of the streaming, if None last forever
         :param path: file's location where saving the data collected, if None print on the std output """

        super(Streamer, self).__init__()
        self.api = api
        self.time_limit = time_limit
        self.path = path
        self.start_time = 0
        self.file = None

    def on_connect(self):

        """ called when the connection with
                the streaming server is established """

        self.start_time = utils.get_time()
        self.on_start()

    def on_error(self, status_code):
        print(status_code)

    def on_data(self, raw_data):

        """ called when raw data is received from stream """

        if self.time_limit is not None and (utils.get_time() - self.start_time) > self.time_limit:
            # stop streaming
            if self.file is not None:
                self.file.close()
                self.file = None
            return False
        else:
            self.process_data(raw_data)
            return True

    @abstractmethod
    def process_data(self, raw_data):
        pass

    @abstractmethod
    def on_start(self):
        pass

    def stream(self, follow=None, track=None, is_async=False, locations=None,
               stall_warnings=False, languages=None, encoding='utf8', filter_level=None):

        """ start the streaming in according to the filtering options passed as parameters """

        stream_ = tweepy.Stream(auth=self.api.auth, listener=self)
        stream_.filter(follow=follow, track=track, is_async=is_async, locations=locations,
                       stall_warnings=stall_warnings, languages=languages, encoding=encoding, filter_level=filter_level)


class OfflineStreamer(Streamer):

    def __init__(self, api, path, time_limit=None):

        """ Offline streamer, requires a path where saving the streaming data """

        super(OfflineStreamer, self).__init__(api, time_limit=time_limit, path=path)

    def process_data(self, raw_data):
        # print the raw data on the file
        self.file.write(raw_data)
        self.file.write("\n")

    def on_start(self):
        try:
            self.file = open(self.path, "a")
        except FileNotFoundError:
            self.file = open(self.path, "w")


class OnlineStreamer(Streamer):

    def __init__(self, api, time_limit=None):

        """ Online streamer, collects data online during streaming
        w/o saving it into a specific text file """

        super(OnlineStreamer, self).__init__(api=api, time_limit=time_limit, path=None)

    def process_data(self, raw_data):
        # TODO: implement online
        pass

    def on_start(self):
        # do nothing
        pass
