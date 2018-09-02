import requests_cache
import json
from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

day_difference = timedelta(days=7)
requests_cache.install_cache(expire_after=day_difference)


@api_view(['GET'])
def get_about_us(request):
    """
    Returns About US content from static JSON file '/api/resources/about-us.json'
    :param request:
    :return: 200 successful
    """
    try:
        filename = 'api/resources/about-us.json'
        file = open(filename, 'r')
        data = file.read()
        data = json.loads(data)
        file.close()
    except (IOError, ValueError):
        data = {"description": "Error in fetching content."}
        return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_help(request):
    """
    Returns HELP content from static JSON file '/api/resources/help.json'
    :param request:
    :return: 200 successful
    """
    try:
        filename = 'api/resources/help.json'
        file = open(filename, 'r')
        data = file.read()
        data = json.loads(data)
        file.close()
    except (IOError, ValueError):
        data = {"help": ["Error in fetching content."]}
        return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data, status=status.HTTP_200_OK)
