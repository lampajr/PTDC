# PTDC: PYTHON TWITTER DATA COLLECTOR


[![Author](http://img.shields.io/badge/author-lampajr-blue.svg?style=flat-square)]
[![PyPi](https://img.shields.io/pypi/v/ptdc.svg?style=flat-square)](https://pypi.org/project/ptdc/)
[![Python 3.7](https://img.shields.io/pypi/pyversions/ptdc.svg)]
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](https://github.com/lampajr/PTDC/blob/master/LICENSE)

Python Twitter data collector built on [Tweepy](https://github.com/tweepy/tweepy) that allow users to dynamically 
collect accounts and statuses from Twitter during streaming, and automatically generate Datasets from collected data
that you can as CSV.

This library provides a framework that you can use to build your own data collector, specifying which are your features
that have to be extracted from Twitter accounts/statuses.

Creating your Twitter dataset:
1. Instantiate an `AccountCollector` and/or `StatusCollector` class in according to what you want collect, accounts, statuses or both.
At this step you can re-defined your own features that have to be extracted from twitter data, you have to pass dict-like parameters in the following form: <feature_name, function> where the function has to be applied to the user or status object.
Please refer to [documentation](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object.html) for more details about Twitter objects
2. Instantiate the `OnlineStreamer` passing the collector as parameter 
3. Start streaming on some topics
4. Save the created dataset at specified location

NB: It is not mandatory to use both collectors and streamer but you can also use Collectors alone, for instance if you already have the users and/or statuses to collect and you don't need to stream anything.

## INSTALLATION

The package is available on PyPi [here](https://pypi.org/project/ptdc/)

```bash
$ pip install ptdc
```

## EXAMPLE USAGE
### Import modules
```
from ptdc import authenticate, AccountCollector, OnlineStreamer, StatusCollector
```
### Define tokens
Replace the following tokens with yours, see Twitter developers [authentication](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html) for more details about how obtain them.
```    
consumer_key = "xxxxxxxxxxx"
consumer_key_secret = "xxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxx"
```    
### Create the default Tweepy API object of tweepy

```
api = authenticate(consumer_key=consumer_key, consumer_key_secret=consumer_key_secret, access_token=access_token, access_token_secret=access_token_secret)
```                       

### Create your own Collectors for collecting data
Create your own StatusCollector object

```
s_collector = StatusCollector(api=api)
```    

Create your own AccountCollector object, which will collect also statuses 
```
collector = AccountCollector(api=api, statuses_collector=s_collector)
```
### Create the Streamer
Create Online Streamer that will collect data (in this case will collect only 5 accounts)
```
streamer = OnlineStreamer(api=api, collector=collector, data_limit=5, n_statuses=400)
```
### Start streaming
You can start streaming in all ways defined by Tweepy, see its doc for more details
```
streamer.stream(track=['famous', 'web', 'vip', 'holiday', 'pic', 'photo'], is_async=False)
```
### Save dataset/s
After streaming ended (in according to your defined limits), save DataFrame/s generated into csv file/s.
You just need to access the collector object and call the save_dataset method providing the path.
```
streamer.collector.save_dataset(path="../data/accounts.csv")
```    
## Questions and Contributing

Feel free to post questions and problems on the issue tracker. Pull requests are welcome!

Feel free to fork and modify or add new features and functionality to the library
