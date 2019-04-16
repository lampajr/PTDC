from ptdc.data import *

if __name__ == '__main__':
    dataset = create_twitter_account_dataframe()
    print(dataset.head())