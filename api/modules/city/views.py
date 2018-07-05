import requests
import requests_cache
from datetime import timedelta

from django.db.models import Count
from requests_oauthlib import OAuth1
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.modules.city.constants import TWITTER_CONSUMER_KEY, TWITTER_OAUTH_TOKEN_SECRET, TWITTER_OAUTH_TOKEN, \
    TWITTER_CONSUMER_SECRET, TWITTER_API_URL
from api.models import City, CityFact, CityImage, CityVisitLog
from api.modules.city.serializers import AllCitiesSerializer, CitySerializer, CityImageSerializer, CityFactSerializer, \
    CityVisitSerializer

hour_difference = timedelta(hours=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_all_cities(request, no_of_cities=8):
    """
    Returns a list of cities with maximum number of logs (visits)
    :param request:
    :param no_of_cities: (default count: 8)
    :return: 200 successful
    """
    cities = City.objects.annotate(visit_count=Count('logs')).order_by('-visit_count')[:no_of_cities]
    serializer = AllCitiesSerializer(cities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_city(request, city_id):
    """
    Returns a city on the basis of city id
    :param request:
    :param city_id:
    :return: 404 if invalid city id is sent
    :return: 200 successful
    """
    try:
        city = City.objects.get(pk=city_id)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Add city visit log
    try:
        city_visit_log = CityVisitLog(city=city, user=request.user)
        city_visit_log.save()
    except Exception as e:
        pass

    serializer = CitySerializer(city)
    return Response(serializer.data)


@api_view(['GET'])
def get_city_by_name(request, city_prefix):
    """
    Returns a list of cities that starts with the given city prefix
    :param request:
    :param city_prefix:
    :return: 200 successful
    """
    cities = City.objects.filter(city_name__istartswith=city_prefix)[:5]
    serializer = AllCitiesSerializer(cities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_city_images(request, city_id):
    """
    Returns a list of all the images for a given city id
    :param request:
    :param city_id:
    :return: 404 if invalid city id is sent
    :return: 200 successful
    """
    try:
        city_images = CityImage.objects.filter(city=city_id)
    except CityImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CityImageSerializer(city_images, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_city_facts(request, city_id):
    """
    Returns a list of all the facts for a given city id
    :param request:
    :param city_id:
    :return: 404 if invalid city id is sent
    :return: 200 successful
    """
    try:
        city_facts = CityFact.objects.filter(city=city_id)
    except CityFact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CityFactSerializer(city_facts, many=True)
    return Response(serializer.data)


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
            url = TWITTER_API_URL + "closest.json?lat={0}&long={1}".format(city.latitude, city.longitude)
            woeid_response = requests.get(url, auth=twitter_auth)
            city.woeid = woeid_response.json()[0]['woeid']
            city.save()
        except Exception as e:
            return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    try:
        url = TWITTER_API_URL + "place.json?id={0}".format(city.woeid)
        api_response = requests.get(url, auth=twitter_auth)
        response = api_response.json()[0]['trends']
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response)


@api_view(['GET'])
def get_city_visits(request):
    """
    Returns a list of cities visited by a user
    :param request:
    :return: 404 if user not authenticated
    :return: 200 successful
    """
    city_visits = CityVisitLog.objects.filter(user=request.user).values('city_id').annotate(total=Count('city'))
    for visit in city_visits:
        obj = City.objects.get(id=visit['city_id'])
        visit['city_name'] = obj.city_name

    serializer = CityVisitSerializer(city_visits, many=True)
    return Response(serializer.data)
