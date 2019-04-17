import tweepy
from ptdc.streamer import OnlineStreamer
import logging
import sys

if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    consumer_key = "ouij6TL9OLOTb3Ca3lcyQ8yUd"
    consumer_key_secret = "VLHEEt5wbB5Kfu5eX1n546CbMSWLJmFuE5c2386u4ljT1uJA71"
    access_token = "425255853-66oQZ4Nw1c6rrjBL2f1M7dkucrrfeYqmUJMAcGfT"
    access_token_secret = "J4OaU6rBjGyr7NBS4CyfY9CPaaeflRT7MVDbk2hFuMFMo"

    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)

    streamer = OnlineStreamer(api=api, time_limit=10)
    streamer.stream(track=['python'])
    streamer.collector.user_dataset_to_csv(filename="../data/accounts.csv")
    streamer.collector.tweets_dataset_to_csv(filename="../data/tweets.csv")