import os
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

from src.logger import initialize_logger
from src.tweets_getter import Tweets
from src.parser import *


def main():
    bearer_token = os.environ.get("bearer-token")
    tweets = Tweets(bearer_token, "z")
    tweets_content = tweets.get_tweets(1)
    tweets.save_tweets()
    logger.success("Tweets saved")
    
    contents = convert_tweets_file_content_to_list(tweets_content)
    download_packages()
    for tweet in tqdm(contents):
        tweet_list = text_to_list(tweet)
        tweet_alpha_lowercase_only = alpha_lowercase_list(tweet_list)
        tweet_sorted = sorted_without_duplicates_list(tweet_alpha_lowercase_only)
        nouns_list = extract_nouns(tweet_sorted)



if __name__ == "__main__":
    load_dotenv()
    initialize_logger()
    main()
