import requests
import request_cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.modules.zomato.zomato_response import Zomato_Response as Food


@api_view(['GET'])
def get_restaurants_all(request,latitude,longitude):

    try:
        api_key = "4425d1bbdbeebc5c39befe14df78459f"
        baseurl = "https: // developers.zomato.com/api/v2.1/geocode?
        lat, long = str(latitude), str(longitude)
        comp = baseurl+lat+'&'+long
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": api_key}
        req = requests.get(comp, headers=header)
        all_details = req.json()
        
        response = []
        for rest in all_details['nearby_restaurants']:
            food = rest['restaurants']
            response.append(Food(id = food['id'],
                                name = food['name'],
                                url = food['url'],
                                latitude=food['location']['latitude'],
                                longitude= food['location']['longitude'],
                                avg2 = food['average_cost_for_two'],
                                currency = food['currency'],
                                image=food['featured_image'],
                                rating = food['user_rating']['aggregate_rating'],
                                votes = food['user_rating']['votes'],
                                try:
                                    phone_numbers = food['phone_numbers']
                                except:
                                    pass
                                ).to_json())
        return Response(response)
