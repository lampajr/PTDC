from ptdc import authenticate, AccountCollector

if __name__ == '__main__':
    consumer_key = "ouij6TL9OLOTb3Ca3lcyQ8yUd"
    consumer_key_secret = "VLHEEt5wbB5Kfu5eX1n546CbMSWLJmFuE5c2386u4ljT1uJA71"
    access_token = "425255853-3ef7FnzN0jHSWUSvgspeUvY95JG5BuYIbnFCwklt"
    access_token_secret = "9rMD6xueUq5iQ5yuv1ZhCznk9AA3LxKOKwlB3HoDLYNUt"

    # Create the default API object of tweepy using provided authentication method
    api = authenticate(consumer_key=consumer_key,
                       consumer_key_secret=consumer_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

    # Create your own AccountCollector, without collecting statuses but only timeline's information
    collector = AccountCollector(api=api)

    # screen names of accounts to collect
    users_to_collect = ["AndreaLampa95"]

    # number of statuses to collect for retrieving infos
    n_statuses = 100

    for name in users_to_collect:
        collector.collect_account(screen_name=name, n_statuses=n_statuses)

    # Save dataset
    collector.save_dataset(path="../data/accounts.csv")
