import requests
import os

from json import dump
from tqdm import tqdm
from loguru import logger
from src.settings import get_settings

MAX_RESULTS_PER_PAGE = get_settings()["MAX_RESULTS_PER_PAGE"]

class Tweets:
    @logger.catch
    def __init__(cls, bearer_token, *keywords) -> None:
        cls.__tweets_path = get_settings()["TWEETS_PATH"]
        cls.tweets = list()
        cls.__headers = cls.__create_headers(bearer_token)
        cls.__query = cls.__create_query(keywords)

    @logger.catch
    def get_tweets(cls, number_of_tweets=10):
        try:
            next_token = dict()
            for _ in tqdm(range(int(number_of_tweets / MAX_RESULTS_PER_PAGE) + 1)):
                url, query_params = cls.__create_url(cls.__query, next_token)
                json_response = cls.__connect_to_endpoint(url, cls.__headers, query_params, next_token)
                if not json_response:
                    raise RuntimeError(f"Got empty response. Query: {cls.__query}")
                next_token = json_response["meta"]["next_token"]
                cls.tweets.append(json_response)
            return cls.tweets
        except RuntimeError as re:
            logger.error(re)

    @logger.catch
    def save_tweets(cls, tweets=None) -> None:
        if not tweets:
            with open(cls.__tweets_path, "w") as f:
                dump(cls.tweets, f)
        else:
            with open(cls.__tweets_path, "w") as f:
                dump(tweets, f)

    @logger.catch
    def __create_headers(cls, bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    @logger.catch
    def __create_query(cls, keywords: list):
        query = str()
        for index, el in enumerate(keywords):
            if index % 2 == 0:
                query += el
            else:
                query += " OR "
                query += el
        query += " lang:en"
        return query

    @logger.catch
    def __create_url(cls, keyword, next_token={}):
        """
        search_url to url do endpointa
        query_params sa zalezne od endpointu
        """
        search_url = "https://api.twitter.com/2/tweets/search/recent"
        
        #search_url = "https://api.twitter.com/2/tweets/search/recent" #Change to the endpoint you want to collect data from

        #change params based on the endpoint you are using

        # query_params = {'query': keyword,
        #                 'start_time': start_date,
        #                 'end_time': end_date,
        #                 'max_results': max_results,
        #                 'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
        #                 'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
        #                 'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
        #                 'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
        #                 'next_token': {}}
        query_params = {
            'query': keyword,
            'next_token': next_token
        }
        return search_url, query_params

    @logger.catch
    def __connect_to_endpoint(cls, url, headers, params, next_token = None):
        params['next_token'] = next_token   #params object received from create_url function
        response = requests.request("GET", url, headers = headers, params = params)
        print("Endpoint Response Code: " + str(response.status_code))
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()



if __name__ == "__main__":
    raise NotImplementedError("Use as class")