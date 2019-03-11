import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.modules.github.utils import make_github_issue
from api.modules.ways.constants import PLACE_AUTOCOMPLETE_API_URL
from api.modules.ways.constants import PLACE_SEARCH_API_URL
from api.modules.ways.constants import PLACE_DETAIL_API_URL
from api.modules.ways.constants import DISTANCE_MATRIX_API_URL


@api_view(['GET'])
def get_ways_train(request, origin, destination):
    """
    :param request:
    :param origin:
    :param destination:
    :return: 503 if API fails due to server error
    :return: 401 if API fails due to authentication error
    :return: 403 Forbidden
    """
    flag = False
    try:
        place_autocomplete_api_response = requests.get(
            PLACE_AUTOCOMPLETE_API_URL.format(destination)
        )
        place_autocomplete_api_response_json = place_autocomplete_api_response.json()
        place_id = place_autocomplete_api_response_json['predictions'][0]['place_id']
        place_detail_api_response = requests.get(PLACE_DETAIL_API_URL.format(place_id))
        place_detail_api_response_json = place_detail_api_response.json()
        address_components = place_detail_api_response_json['result']['address_components']
        all_address_components = len(address_components)
        city = []
        for i in range(0, all_address_components):
            all_types = len(['types'])
            for j in range(0, all_types):
                if address_components[i]['types'][j] == 'locality':
                    city.append(address_components[i]['long_name'])

        for i in range(0, all_address_components):
            all_types = len(['types'])
            for j in range(0, all_types):
                if address_components[i]['types'][j] == 'administrative_area_level_1':
                    city.append(address_components[i]['long_name'])
        place_search_api_response = requests.get(
            PLACE_SEARCH_API_URL.format(city, 'train_station')
            )
        place_search_api_response_json = place_search_api_response.json()

        station_place_id = place_search_api_response_json['results'][0]['place_id']
        station_name = place_search_api_response_json['results'][0]['name']
        distance_api_response = requests.get(
            DISTANCE_MATRIX_API_URL.format('place_id:'+place_id, 'place_id:'+station_place_id,  walk_or_drive='driving')
            )
        distance_api_response_json = distance_api_response.json()
        distance = distance_api_response_json['rows'][0]['elements'][0]['distance']['text']
        duration = distance_api_response_json['rows'][0]['elements'][0]['duration']['text']
        response_string = '{} is {} away from {} station ' \
                          'and can be reached in {} drive.'.format(destination, distance, station_name, duration)
        if place_autocomplete_api_response.status_code == 503:
            error_message = "Places Autocomplete API error - Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if place_autocomplete_api_response.status_code == 401:
            error_message = 'Places Autocomplete API error - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if place_autocomplete_api_response.status_code == 403:
            error_message = 'Places Autocomplete API error - Permission denied/Forbidden'
            flag = True
        if place_search_api_response.status_code == 503:
            error_message = "Places Search API error - Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if place_search_api_response.status_code == 401:
            error_message = 'Places Search API error - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if place_search_api_response.status_code == 403:
            error_message = 'Places Search API error - Permission denied/Forbidden'
            flag = True
        if distance_api_response.status_code == 503:
            error_message = "Distance Matrix API error - Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if distance_api_response.status_code == 401:
            error_message = 'Distance Matrix API error  - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if distance_api_response.status_code == 403:
            error_message = 'Distance Matrix API error  - Permission denied/Forbidden'
            flag = True
        if flag:
            # create GitHub issue to get developer's attention
            make_github_issue(error_message)
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except IndexError as e:
        error_message = 'No place found of given address'
        return Response(error_message, status.HTTP_200_OK)
    except KeyError as e:
        error_message = 'No Route Found'
        return Response(error_message, status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(response_string)


@api_view(['GET'])
def get_ways_flight(request, origin, destination):
    """
    :param request:
    :param origin:
    :param destination:
    :return: 503 if API fails due to server error
    :return: 401 if API fails due to authentication error
    :return: 403 Forbidden
    """
    flag = False
    try:
        place_autocomplete_api_response = requests.get(
            PLACE_AUTOCOMPLETE_API_URL.format(destination)
        )
        place_autocomplete_api_response_json = place_autocomplete_api_response.json()
        place_id = place_autocomplete_api_response_json['predictions'][0]['place_id']
        place_detail_api_response = requests.get(PLACE_DETAIL_API_URL.format(place_id))
        place_detail_api_response_json = place_detail_api_response.json()
        address_components = place_detail_api_response_json['result']['address_components']
        all_address_components = len(address_components)
        city = []
        for i in range(0, all_address_components):
            all_types = len(['types'])
            for j in range(0, all_types):
                if address_components[i]['types'][j] == 'locality':
                    city.append(address_components[i]['long_name'])

        for i in range(0, all_address_components):
            all_types = len(['types'])
            for j in range(0, all_types):
                if address_components[i]['types'][j] == 'administrative_area_level_1':
                    city.append(address_components[i]['long_name'])
        place_search_api_response = requests.get(
            PLACE_SEARCH_API_URL.format(city, 'airport')
            )
        place_search_api_response_json = place_search_api_response.json()
        airport_place_id = place_search_api_response_json['results'][0]['place_id']
        airport = place_search_api_response_json['results'][0]['name']
        distance_api_response = requests.get(
            DISTANCE_MATRIX_API_URL.format('place_id:' + place_id, 'place_id:' + airport_place_id,
                                           walk_or_drive='driving')
            )
        distance_api_response_json = distance_api_response.json()
        distance = distance_api_response_json['rows'][0]['elements'][0]['distance']['text']
        duration = distance_api_response_json['rows'][0]['elements'][0]['duration']['text']
        response_string = '{} is {} away from {} airport ' \
                          'and can be reached in {} drive.'.format(destination, distance, airport, duration)

        if place_autocomplete_api_response.status_code == 503:
            error_message = "Places Autocomplete API error - Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if place_autocomplete_api_response.status_code == 401:
            error_message = 'Places Autocomplete API error - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if place_autocomplete_api_response.status_code == 403:
            error_message = 'Places Autocomplete API error - Permission denied/Forbidden'
            flag = True
        if place_search_api_response.status_code == 503:
            error_message = "Places Search API error - Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if place_search_api_response.status_code == 401:
            error_message = 'Places Search API error - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if place_autocomplete_api_response.status_code == 403:
            error_message = 'Places API error - Permission denied/Forbidden'
            flag = True
        if distance_api_response.status_code == 503:
            error_message = "Distance Matrix API error - Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if distance_api_response.status_code == 401:
            error_message = 'Distance Matrix API error - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if distance_api_response.status_code == 403:
            error_message = 'Distance Matrix API error  - Permission denied/Forbidden'
            flag = True
        if flag:
            # create GitHub issue to get developer's attention
            make_github_issue(error_message)
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except IndexError as e:
        error_message = 'No place found of given address'
        return Response(error_message, status.HTTP_200_OK)
    except KeyError as e:
        error_message = 'No Route Found'
        return Response(error_message, status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(response_string)


@api_view(['GET'])
def get_ways_road(request, origin, destination, mode):
    """
    :param request:
    :param origin:
    :param destination:
    :param mode:
    :return: 503 if API fails due to server error
    :return: 401 if API fails due to authentication error
    :return: 403 Forbidden
    """
    flag = False
    try:
        place_autocomplete_api_response = requests.get(
            PLACE_AUTOCOMPLETE_API_URL.format(origin)
        )
        place_autocomplete_api_response_json = place_autocomplete_api_response.json()
        origin_place_id = place_autocomplete_api_response_json['predictions'][0]['place_id']
        place_autocomplete_api_response = requests.get(
            PLACE_AUTOCOMPLETE_API_URL.format(destination)
        )
        place_autocomplete_api_response_json = place_autocomplete_api_response.json()
        destination_place_id = place_autocomplete_api_response_json['predictions'][0]['place_id']
        distance_api_response = requests.get(
            DISTANCE_MATRIX_API_URL.format('place_id:' + origin_place_id, 'place_id:' + destination_place_id,
                                           walk_or_drive=mode)
            )
        distance_api_response_json = distance_api_response.json()
        distance = distance_api_response_json['rows'][0]['elements'][0]['distance']['text']
        duration = distance_api_response_json['rows'][0]['elements'][0]['duration']['text']
        response_string = '{} is {} away from {}  ' \
                          'and can be reached in {} by {}.'.format(origin, distance, destination, duration, mode)
        if place_autocomplete_api_response.status_code == 503:
            error_message = "Places Autocomplete API error - Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if place_autocomplete_api_response.status_code == 401:
            error_message = 'Places Autocomplete API error - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if place_autocomplete_api_response.status_code == 403:
            error_message = 'Places Autocomplete API error - Permission denied/Forbidden'
            flag = True
        if distance_api_response.status_code == 503:
            error_message = "Distance Matrix API - Service Unavailable"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if distance_api_response.status_code == 401:
            error_message = 'Distance Matrix API - Invalid authentication'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if distance_api_response.status_code == 403:
            error_message = 'Distance Matrix API - Permission denied/Forbidden'
            flag = True
        if flag:
            # create GitHub issue to get developer's attention
            make_github_issue(error_message)
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        error_message = 'No Route Found'
        return Response(error_message, status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(response_string)
