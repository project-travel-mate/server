from datetime import timedelta

import requests
import requests_cache
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api.models import City, CityFact, CityImage, CityVisitLog, Trip
from api.modules.city.serializers import CityCondensedSerializer, CitySerializer, CityImageSerializer, \
    CityFactSerializer
from api.modules.city.utils import extract_as_dict, clean_wiki_extract

seven_day_difference = timedelta(days=7)
requests_cache.install_cache(expire_after=seven_day_difference)


@api_view(['GET'])
def get_all_cities(request):
    """
    Returns a list of cities with maximum number of logs (visits)
    :param request:
    :return: 200 successful
    """
    cities = City.objects.annotate(visit_count=Count('logs')).order_by('-visit_count')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    cities_paginated = paginator.paginate_queryset(cities, request)
    serializer = CityCondensedSerializer(cities_paginated, many=True)
    return paginator.get_paginated_response(serializer.data)


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
        city.has_visited = Trip.objects.filter(city=city, users=request.user).exists()

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
    serializer = CityCondensedSerializer(cities, many=True)
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

    paginator = PageNumberPagination()
    paginator.page_size = 10
    city_images_paginated = paginator.paginate_queryset(city_images, request)
    serializer = CityImageSerializer(city_images_paginated, many=True)
    return paginator.get_paginated_response(serializer.data)


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

    paginator = PageNumberPagination()
    paginator.page_size = 10
    city_facts_paginated = paginator.paginate_queryset(city_facts, request)
    serializer = CityFactSerializer(city_facts_paginated, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def get_city_information(request, city_id):
    """
    Return detail of city extracted using wikipedia api
    :param request:
    :param city_id:
    :return: 503 if wiki api fails
    :return: 404 if city is not found
    :return: 200 successful
    """
    try:
        city = City.objects.get(id=city_id)
        wiki_api_url = "https://en.wikipedia.org/w/api.php" + \
                       "?action=query&prop=extracts&explaintext&titles=" + \
                       city.city_name + \
                       "&format=json"
        api_response = requests.get(wiki_api_url)
        data = api_response.json()
        # fetching unique number associated with every city as a key in response
        city_wiki_number = list((data['query']['pages']).keys())[0]
        extract = data['query']['pages'][city_wiki_number]['extract']
        extract = clean_wiki_extract(extract)
        city_detail = extract_as_dict(extract)
    except City.DoesNotExist:
        error_message = "City does not exist"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(city_detail, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_visited_city(request, user_id=None):
    """
    all the unique cities user has in his list of trips.
    :param request:
    :param user_id:
    :return: 404 if user does not exist
    :return: 200 successful
    """
    # if user with user_id does not exist
    if not user_id:
        user_id = request.user.id

    if not User.objects.filter(id=user_id).exists():
        error_message = "User does not exists."
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)

    cities = set()
    trips = Trip.objects.filter(users=user_id)
    for trip in trips:
        cities.add(trip.city)
    serializer = CityCondensedSerializer(cities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
