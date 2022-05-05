# For sending GET requests from the API
import requests

# For saving access tokens and for file management when creating and adding to the dataset
import os

# For dealing with json responses we receive from the API
import json

# For displaying the data after
import pandas as pd

# For saving the response data in CSV format
import csv

# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata

# To add wait time between requests
import time
from dotenv import load_dotenv
from loguru import logger

from src.logger import initialize_logger


def auth():
    return os.environ.get("bearer-token")


def main():
    logger.success("Good")


if __name__ == "__main__":
    load_dotenv()
    initialize_logger()
    main()
