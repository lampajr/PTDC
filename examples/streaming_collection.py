from ptdc.streamer import OnlineStreamer
from ptdc.collector import AccountCollector
from ptdc.support import authenticate

if __name__ == '__main__':
    """
    consumer_key = "xxxxxxxxxxxx"
    consumer_key_secret = "xxxxxxxxxxxxxx"
    access_token = "xxxxxxxxxxxxxxxxxxxxxxxx"
    access_token_secret = "xxxxxxxxxxxxxx"
    """

    consumer_key = "ouij6TL9OLOTb3Ca3lcyQ8yUd"
    consumer_key_secret = "VLHEEt5wbB5Kfu5eX1n546CbMSWLJmFuE5c2386u4ljT1uJA71"
    access_token = "425255853 - 66oQZ4Nw1c6rrjBL2f1M7dkucrrfeYqmUJMAcGfT"
    access_token_secret = "J4OaU6rBjGyr7NBS4CyfY9CPaaeflRT7MVDbk2hFuMFMo"

    # Create the default API object of tweepy using provided authentication method
    api = authenticate(consumer_key=consumer_key,
                       consumer_key_secret=consumer_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

    # Create your own AccountCollector, without collecting statuses but only timeline's information
    collector = AccountCollector(api=api)

    # Create Online Streamer that will collect data for 45 seconds
    # Using collector=None the streamer will create a default collector
    streamer = OnlineStreamer(api=api,
                              collector=collector,
                              n_statuses=3200)

    # Start streaming on some topics, on the current thread
    streamer.stream(track=['famous', 'web', 'vip'], is_async=False)

    # After streaming ended, save DataFrame generated into csv files
    streamer.collector.user_dataset_to_csv(filename="../data/accounts.csv")
    streamer.collector.statuses_dataset_to_csv(filename="../data/statuses.csv")