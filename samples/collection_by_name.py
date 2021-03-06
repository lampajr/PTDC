import sys

from ptdc import authenticate, AccountCollector

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

    # Create your own AccountCollector, without collecting timeline's information
    collector = AccountCollector(api=api, timeline_features={})

    # screen names of accounts to collect
    users_to_collect = ["Diletta Leotta", "lampajr", "rami kantari"]

    for name in users_to_collect:
        collector.collect_users_by_name(name, 10)

    # Save dataset
    collector.save_dataset(path="../dataset/similar.csv")
