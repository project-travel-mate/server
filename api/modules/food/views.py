import requests
from rest_framework.decorators import api_view
import requests_cache
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from api.modules.food.constants import BASE_URL, header
from api.modules.food.zomato_response import ZomatoResponse 


hour_difference = timedelta(hours=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_all_restaurants(request, latitude, longitude):
    response = []
    """
    Returns restaurant details forecast for given city using coordinates
    :param request:
    :param latitude:
    :param longitude:
    :return: 503 if Zomato api fails
    :return: 200 successful
    """

    try:

        latitude_user, longitude_user = 'lat=' + latitude, 'lon=' + longitude
        comp = BASE_URL+latitude_user+'&'+longitude_user
        req = requests.get(comp, headers=header)
        all_details = req.json()
        if not req.ok:
            error_message = all_details['message']
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        for rest in all_details['nearby_restaurants']:
            food = rest['restaurant']
            response.append(ZomatoResponse(id=food['id'],
                            name=food['name'],
                            url=food['url'],
                            latitude=food['location']['latitude'],
                            longitude=food['location']['longitude'],
                            avg2=food['average_cost_for_two'],
                            currency=food['currency'],
                            image=food['featured_image'],
                            rating=food['user_rating']['aggregate_rating'],
                            votes=food['user_rating']['votes']).to_json())

    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response)
