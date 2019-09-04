from datetime import timedelta

import requests
import requests_cache
from requests_oauthlib import OAuth1
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.commonresponses import DOWNSTREAM_ERROR_RESPONSE
from api.models import City
from api.modules.twitter.constants import TWITTER_CONSUMER_KEY, TWITTER_OAUTH_TOKEN_SECRET, TWITTER_OAUTH_TOKEN, \
    TWITTER_CONSUMER_SECRET, TWITTER_TRENDS_URL, TWITTER_SEARCH_URL
from api.modules.twitter.twitter_response import SearchTweetResponse

hour_difference = timedelta(hours=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_city_trends(request, city_id):
    """
    Returns a list of top trending tweets in the given city
    :param request:
    :param city_id:
    :return: 404 if invalid city id is sent
    :return: 503 if Twitter API request fails
    :return: 200 successful
    """
    try:
        city = City.objects.get(pk=city_id)
    except City.DoesNotExist:
        error_message = "Invalid City ID"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)

    twitter_auth = OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_OAUTH_TOKEN,
                          TWITTER_OAUTH_TOKEN_SECRET)

    # check if city WOEID is in database or not
    if not city.woeid:
        try:
            url = TWITTER_TRENDS_URL + "closest.json?lat={0}&long={1}".format(city.latitude, city.longitude)
            woeid_response = requests.get(url, auth=twitter_auth)
            city.woeid = woeid_response.json()[0]['woeid']
            city.save()
        except Exception as e:
            return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    try:
        url = TWITTER_TRENDS_URL + "place.json?id={0}".format(city.woeid)
        api_response = requests.get(url, auth=twitter_auth)
        response = api_response.json()[0]['trends']
    except Exception:
        return DOWNSTREAM_ERROR_RESPONSE

    return Response(response)


@api_view(['GET'])
def get_search_tweets(request, query):
    """
    Returns a list of related tweets for given search query
    :param request:
    :param queryf:
    :return: 503 if Twitter API request fails
    :return: 200 successful
    """
    twitter_auth = OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_OAUTH_TOKEN,
                          TWITTER_OAUTH_TOKEN_SECRET)
    try:
        url = TWITTER_SEARCH_URL + "tweets.json?q={0}".format(query)
        api_response = requests.get(url, auth=twitter_auth)
        api_response_json = api_response.json()
        tweets = api_response_json['statuses']
        response = []
        for tweet in tweets:
            result = SearchTweetResponse(
                created_at=tweet['created_at'],
                text=tweet['text'],
                username=tweet['user']['screen_name'],
                user_screen_name=tweet['user']['name'],
                user_profile_image=tweet['user']['profile_image_url'],
                retweet_count=tweet['retweet_count'],
                favorite_count=tweet['favorite_count'],
                tweet_url="https://www.twitter.com/" + tweet['user']['screen_name'] + "/status/" + tweet['id_str'],
            )
            result_as_json = result.to_json()
            response.append(result_as_json)

    except Exception:
        return DOWNSTREAM_ERROR_RESPONSE

    return Response(response)
