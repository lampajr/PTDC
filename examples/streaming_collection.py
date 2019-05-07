import sys

from ptdc import authenticate, AccountCollector, OnlineStreamer

if __name__ == '__main__':

    if len(sys.argv) == 5:
        consumer_key = sys.argv[1]
        consumer_key_secret = sys.argv[2]
        access_token = sys.argv[3]
        access_token_secret = sys.argv[4]
    else:
        consumer_key = "xxxxxxxxxxxx"
        consumer_key_secret = "xxxxxxxxxxxxxx"
        access_token = "xxxxxxxxxxxxxxxxxxxxxxxx"
        access_token_secret = "xxxxxxxxxxxxxx"

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