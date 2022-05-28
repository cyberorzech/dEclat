import os
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

from src.logger import initialize_logger
from src.tweets_getter import Tweets
from src.parser import *


def main():    
    bearer_token = os.environ.get("bearer-token")

    # source data1: poland and ukraine
    tweets = Tweets(bearer_token, "poland", "ukraine")
    tweets_content = tweets.get_tweets(number_of_tweets=50000)
    tweets.save_tweets()
    logger.success("Tweets saved")
    
    contents = convert_tweets_file_content_to_list(tweets_content)
    download_packages()
    declat_input = list() # pandas
    for tweet in tqdm(contents):
        tweet_list = text_to_list(tweet)
        tweet_alpha_lowercase_only = alpha_lowercase_list(tweet_list)
        tweet_sorted = sorted_without_duplicates_list(tweet_alpha_lowercase_only)
        tweet_nouns = list()
        for word in tweet_sorted:
            if not is_noun(word):
                continue
            tweet_nouns.append(word)
        if len(tweet_nouns) == 0:
            continue
        declat_input.append(tweet_nouns)
    
    declat_input = add_padding_to_tweet_lists(declat_input)
    declat_input = convert_list_of_lists_to_df(declat_input)
    declat_input.to_csv("fixtures/datasource_1.csv", sep=";", index=False)
        
    # source data2: cybersecurity, AI
    tweets = Tweets(bearer_token, "cybersecurity", "artificial", "intelligence")
    tweets_content = tweets.get_tweets(number_of_tweets=50000)
    tweets.save_tweets()
    logger.success("Tweets saved")
    
    contents = convert_tweets_file_content_to_list(tweets_content)
    download_packages()
    declat_input = list() # pandas
    for tweet in tqdm(contents):
        tweet_list = text_to_list(tweet)
        tweet_alpha_lowercase_only = alpha_lowercase_list(tweet_list)
        tweet_sorted = sorted_without_duplicates_list(tweet_alpha_lowercase_only)
        tweet_nouns = list()
        for word in tweet_sorted:
            if not is_noun(word):
                continue
            tweet_nouns.append(word)
        if len(tweet_nouns) == 0:
            continue
        declat_input.append(tweet_nouns)
    
    declat_input = add_padding_to_tweet_lists(declat_input)
    declat_input = convert_list_of_lists_to_df(declat_input)
    declat_input.to_csv("fixtures/datasource_2.csv", sep=";", index=False)



if __name__ == "__main__":
    load_dotenv()
    initialize_logger()
    main()
