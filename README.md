# PTDC: PYTHON TWITTER DATA COLLECTOR

### Python library that provides methods useful for collecting data from Twitter Social Network.

## INSTALLATION
##### type the following command:
    ~$ pip install --index-url https://test.pypi.org/simple/ ptdc

## USAGE
### Import modules
    from ptdc import streamer as st
    from ptdc import support as sp
   
### Define tokens
    # change these tokens with yours, see Twitter develeopers for more details to how obtain them
    consumer_key = "fsvd..."
    consumer_key_secret = "derfWdew3..."
    access_token = "dbAD..."
    access_token_secret = "J4O..."
    
### Create the default API object of tweepy
    api = sp.authenticate(consumer_key=consumer_key,
                          consumer_key_secret=consumer_key_secret,
                          access_token=access_token,
                          access_token_secret=access_token_secret)

### Create Online Streamer w/ default collector
    streamer = st.OnlineStreamer(api=api, collector=None, time_limit=45, data_limit=None)

### Start streaming on some topics, on the current thread
    streamer.stream(track=['famous', 'web', 'vip'], is_async=False)

### After streaming ended, save DataFrame generated into csv files
    streamer.collector.user_dataset_to_csv(filename="../data/accounts.csv")
    streamer.collector.tweets_dataset_to_csv(filename="../data/statuses.csv")
