"""
Uses Trends Twitter API
Reference Docs: https://developer.twitter.com/en/docs/trends/trends-for-location/overview
Needs to find a WOEID (Yahoo! Where On Earth ID) for one city and accordingly make the call
"""
import os

TWITTER_API_URL = "https://api.twitter.com/1.1/trends/"

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", None)
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", None)
TWITTER_OAUTH_TOKEN = os.environ.get("TWITTER_OAUTH_TOKEN", None)
TWITTER_OAUTH_TOKEN_SECRET = os.environ.get("TWITTER_OAUTH_TOKEN_SECRET", None)
