import requests
import requests_cache
from datetime import timedelta

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.modules.PlacesAPI.hyperlocal_response import HyperLocalResponse
from api.modules.PlacesAPI.constants import PLACES_SEARCH_API_URL

hour_difference = timedelta(days=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_places(request, latitude, longitude, place_keyword):
    """
        Return list of places matched
        :param request:
        :param latitude:
        :param: longitude:
        :param : place_keyword:
        :return: 503 if Places api fails
        :return: 200 successful
    """
    try:
        api_response = requests.get(
            PLACES_SEARCH_API_URL.format(latitude=latitude, longitude=longitude, place_keyword=place_keyword)
        )
        api_response_json = api_response.json()
        if api_response.status_code == 503:
            error_message = "Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        response = []
        suggestions = api_response_json['results']
        for place in suggestions:
            result = HyperLocalResponse(
                title=place['title'],
                website=place['href'],
                address=place['vicinity'],
            )
            result_as_json = result.to_json()
            response.append(result_as_json)
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response)
