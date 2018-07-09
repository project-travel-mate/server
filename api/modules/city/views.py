from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import City, CityFact, CityImage, CityVisitLog
from api.modules.city.serializers import AllCitiesSerializer, CitySerializer, CityImageSerializer, CityFactSerializer, \
    CityVisitSerializer


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
def get_city_visits(request):
    """
    Returns a list of cities visited by a user
    :param request:
    :return: 404 if invalid user not authenticated
    :return: 200 successful
    """
    city_visits = CityVisitLog.objects.filter(user=request.user).values('city_id').annotate(
        visit_count=Count('city')).order_by('-visit_count')
    for visit in city_visits:
        visit['city'] = City.objects.get(pk=visit['city_id'])

    serializer = CityVisitSerializer(city_visits, many=True)
    return Response(serializer.data)
