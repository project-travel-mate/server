from datetime import timedelta

import requests
import requests_cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.modules.hyperlocal.constants import PLACES_SEARCH_API_URL
from api.modules.hyperlocal.hyperlocal_response import HyperLocalResponse
from api.modules.hyperlocal.utils import make_github_issue
hour_difference = timedelta(days=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_places(request, latitude, longitude, places_query):
    """
    Return list of places matched
    :param request:
    :param latitude:
    :param longitude:
    :param places_query:
    :return: 503 if Places api fails
    :return: 400 if invalid parameters are passed
    :return: 200 successful
    """
    try:
        api_response = requests.get(
            PLACES_SEARCH_API_URL.format(latitude=latitude, longitude=longitude, places_query=places_query)
        )
        api_response_json = api_response.json()
        if api_response.status_code == 503:
            error_message = "Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if api_response.status_code == 401:
            error_message = 'Places API error - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if api_response.status_code == 403:
            error_message = 'Places API error - Incorrect app_code or app_id'
            # todo create issue
            make_github_issue(error_message)
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    response = []
    suggestions = api_response_json['results']['items']
    if len(suggestions) == 0:
        # no related place found
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    for place in suggestions:
        result = HyperLocalResponse(
            title=place['title'],
            website=place['href'],
            address=place['vicinity'],
            icon=place['icon'],
            latitude=place['position'][0],
            longitude=place['position'][1],
            distance=place['distance']
        )
        result_as_json = result.to_json()
        response.append(result_as_json)

    return Response(response)
