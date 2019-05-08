import sys

from ptdc import authenticate, AccountCollector, StatusCollector

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
    s_collector = StatusCollector(api=api)

    # Create your own AccountCollector, without collecting statuses but only timeline's information
    collector = AccountCollector(api=api, statuses_collector=s_collector)

    # screen names of accounts to collect
    users_to_collect = ["", "", ""]

    # number of statuses to collect for retrieving infos
    n_statuses = 3200

    for name in users_to_collect:
        collector.collect_account(screen_name=name, n_statuses=n_statuses)

    # Save dataset
    collector.save_dataset(path="../data/accounts.csv")