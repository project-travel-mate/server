import requests
from rest_framework.decorators import api_view
import requests_cache
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from api.modules.food.constants import BASE_URL, ZOMATO_API_KEY, USER_AGENT, ACCEPT
<<<<<<< HEAD
from api.modules.food.zomato_response import ZomatoResponse
=======
from api.modules.food.zomato_response import ZomatoResponse 
>>>>>>> 2ca36d5... all_changes_made


hour_difference = timedelta(hours=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_all_restaurants(request, latitude, longitude):
    """
    Returns restaurant details forecast for given city using coordinates
    :param request:
    :param latitude:
    :param longitude:
    :return: 503 if Zomato api fails
    :return: 200 successful
    """
    response = []
    try:
        header = {"User-agent": USER_AGENT, "Accept": ACCEPT, "user_key": ZOMATO_API_KEY}
<<<<<<< HEAD
        api_response = requests.get(BASE_URL.format(latitude, longitude), headers=header)
        api_response_json = api_response.json()
        if not api_response.ok:
            error_message = api_response_json['message']
=======
        req = requests.get(BASE_URL.format(latitude,longitude), headers=header)
        all_details = req.json()
        if not req.ok:
<<<<<<< HEAD
            error_message = all_details['message']
>>>>>>> 2ca36d5... all_changes_made
=======
            error_message = """ all_details['message'] """ "Hi"
>>>>>>> 17cebad... minor bugs solved
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        for restaurant inapi_response_json['nearby_restaurants']:
            food = restaurant['restaurant']
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
