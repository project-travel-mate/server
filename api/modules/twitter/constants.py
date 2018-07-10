"""
Uses Twitter API
Reference Docs: https://developer.twitter.com/en/docs/
Needs to find a WOEID (Yahoo! Where On Earth ID) for one city and accordingly make the call
"""
import os

TWITTER_API_URL = "https://api.twitter.com/1.1/"

TWITTER_TRENDS_URL = TWITTER_API_URL + "trends/"
TWITTER_SEARCH_URL = TWITTER_API_URL + "search/"

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", None)
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", None)
TWITTER_OAUTH_TOKEN = os.environ.get("TWITTER_OAUTH_TOKEN", None)
TWITTER_OAUTH_TOKEN_SECRET = os.environ.get("TWITTER_OAUTH_TOKEN_SECRET", None)
