# PTDC: PYTHON TWITTER DATA COLLECTOR

#### Python Tweepy wrapper library that provides methods useful for collecting data from Twitter Social Network and creating new Datasets.

#### Latest Version: 1.1.0
## INSTALLATION
##### type the following command:
    ~$ pip install --index-url https://test.pypi.org/simple/ ptdc

## USAGE
### Import modules
    from ptdc import authenticate, AccountCollector, OnlineStreamer, StatusCollector
   
### Define tokens
    # replace these tokens with yours, see Twitter develeopers for more details to how obtain them
    consumer_key = "xxxxxxxxxxx"
    consumer_key_secret = "xxxxxxxxxxxxx"
    access_token = "xxxxxxxxxxxxxxxxxxxxxx"
    access_token_secret = "xxxxxxxxxxxxxxxxxx"
    
### Create the default API object of tweepy
    api = authenticate(consumer_key=consumer_key,
                       consumer_key_secret=consumer_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)
                       
### Create your own collectors for collect data
    # Create your own StatusCollector
    s_collector = StatusCollector(api=api)

    # Create your own AccountCollector, collecting statuses 
    collector = AccountCollector(api=api, statuses_collector=s_collector)

### Create Online Streamer 
    # Create Online Streamer that will collect data for 45 seconds
    # Using collector=None the streamer will create a default collector
    streamer = OnlineStreamer(api=api,
                              collector=collector,
                              data_limit=5,
                              n_statuses=400)

### Start streaming on some topics, on the current thread
    streamer.stream(track=['famous', 'web', 'vip', 'holiday', 'pic', 'photo'], is_async=False)

### After streaming ended, save DataFrame generated into csv files
    streamer.collector.save_dataset(path="../data/accounts.csv")
