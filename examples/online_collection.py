from ptdc.streamer import OnlineStreamer
from ptdc.support import authenticate

if __name__ == '__main__':
    consumer_key = "fsvd..."
    consumer_key_secret = "derfWdew3..."
    access_token = "dbAD..."
    access_token_secret = "J4O..."

    # Create the default API object of tweepy using provided authentication method
    api = authenticate(consumer_key=consumer_key,
                       consumer_key_secret=consumer_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

    # Create Online Streamer that will collect data for 45 seconds
    # Using collector=None the streamer will create a default collector
    streamer = OnlineStreamer(api=api, collector=None, time_limit=45, data_limit=None)

    # Start streaming on some topics, on the current thread
    streamer.stream(track=['famous', 'web', 'vip'], is_async=False)

    # After streaming ended, save DataFrame generated into csv files
    streamer.collector.user_dataset_to_csv(filename="../data/accounts.csv")
    streamer.collector.tweets_dataset_to_csv(filename="../data/statuses.csv")