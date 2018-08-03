import requests
from rest_framework.decorators import api_view
import requests_cache
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from api.modules.food.zomato_response import ZomatoResponse, ZomatoResponseDetailed
from api.modules.food.constants import BASE_URL, ZOMATO_API_KEY, USER_AGENT, ACCEPT, LIST, RESTAURANT

hour_difference = timedelta(days=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_all_restaurants(request, latitude, longitude):
    """
    Returns restaurant details forecast for given city using coordinates
    :param request:
    :param latitude:
    :param longitude:
    :return: 503 if Zomato API fails
    :return: 200 successful
    """
    response = []
    try:
        header = {"User-agent": USER_AGENT, "Accept": ACCEPT, "user_key": ZOMATO_API_KEY}
        URL = BASE_URL+LIST
        api_response = requests.get(URL.format(latitude, longitude), headers=header)
        api_response_json = api_response.json()
        if not api_response.ok:
            error_message = api_response_json['message']
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        for restaurant in api_response_json['nearby_restaurants']:
            restaurant_obj = restaurant['restaurant']
            response.append(ZomatoResponse(id=restaurant_obj['id'],
                            name=restaurant_obj['name'],
                            url=restaurant_obj['url'],
                            latitude=restaurant_obj['location']['latitude'],
                            longitude=restaurant_obj['location']['longitude'],
                            avg2=restaurant_obj['average_cost_for_two'],
                            currency=restaurant_obj['currency'],
                            image=restaurant_obj['featured_image'],
                            rating=restaurant_obj['user_rating']['aggregate_rating'],
                            votes=restaurant_obj['user_rating']['votes'],
                            address=restaurant_obj['location']['address']).to_json())

    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response)


@api_view(['GET'])
def get_restaurant(request, restaurant_id):
    """
    Returns restaurant details for a given restaurant id
    :param request:
    :param latitude:
    :param longitude:
    :return: 503 if Zomato API fails
    :return: 200 successful
    """
    try:
        header = {"User-agent": USER_AGENT, "Accept": ACCEPT, "user_key": ZOMATO_API_KEY}
        URL = BASE_URL+RESTAURANT
        api_response = requests.get(URL.format(restaurant_id), headers=header)
        api_response_json = api_response.json()
        if not api_response.ok:
            error_message = api_response_json['message']
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        response = ZomatoResponseDetailed(id=api_response_json['id'],
                                          name=api_response_json['name'],
                                          url=api_response_json['url'],
                                          address=api_response_json['location']['address'],
                                          longitude=api_response_json['location']['longitude'],
                                          latitude=api_response_json['location']['latitude'],
                                          avg2=api_response_json['average_cost_for_two'],
                                          price_range=api_response_json['price_range'],
                                          currency=api_response_json['currency'],
                                          img=api_response_json['featured_image'],
                                          agg_rating=api_response_json['user_rating']['aggregate_rating'],
                                          votes=api_response_json['user_rating']['votes'],
                                          deliver=api_response_json['has_online_delivery'],
                                          booking=api_response_json['has_table_booking'],
                                          cuisines=api_response_json['cuisines'],
                                          ).to_json()
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response)
