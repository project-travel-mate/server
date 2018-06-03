import json

from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.modules.city.model import City, CityImage, CityFact
from api.modules.city.serializers import CitySerializer, CityImageSerializer, CityFactSerializer

@api_view(['GET'])
def get_all_cities(request):
    """
    Returns a list of all the cities
    :param request:
    :return:
    """
    if request.method == 'GET':
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_city(request, city_id):
    """
    Returns a city on the basis of city id
    :param request:
    :param city_id:
    :return:
    """
    try:
        city = City.objects.get(pk=city_id)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CitySerializer(city)
        return Response(serializer.data)


@api_view(['GET'])
def get_all_city_images(request, city_id):
    """
    Returns a list of all the images for a given city id
    :param request:
    :param city_id:
    :return:
    """
    try:
        city_images = CityImage.objects.filter(city=city_id)
    except CityImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CityImageSerializer(city_images, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_all_city_facts(request, city_id):
    """
    Returns a list of all the facts for a given city id
    :param request:
    :param city_id:
    :return:
    """
    try:
        city_facts = CityFact.objects.filter(city=city_id)
    except CityFact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CityFactSerializer(city_facts, many=True)
        return Response(serializer.data)
