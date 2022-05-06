import os
from dotenv import load_dotenv
from loguru import logger

from src.logger import initialize_logger
from src.tweets_getter import Tweets
from src.data_cleaner import *


def main():
    bearer_token = os.environ.get("bearer-token")
    tweets = Tweets(bearer_token, "z")
    tweets_content = tweets.get_tweets(1)
    tweets.save_tweets()
    
    contents = convert_tweets_file_content_to_list(tweets_content)
    print(contents)



if __name__ == "__main__":
    load_dotenv()
    initialize_logger()
    main()
