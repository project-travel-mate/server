import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.modules.weather.constants import OPEN_WEATHER_API_URL, OPEN_FORECAST_API_URL
from api.modules.weather.utils import to_celsius, icon_to_url
from api.modules.weather.weather_response import WeatherResponse


@api_view(['GET'])
def get_city_weather(request, city_name):
    if request.method == 'GET':
        try:
            api_response = requests.get(OPEN_WEATHER_API_URL.format(city_name))
            api_response = api_response.json()

            response = WeatherResponse(temp=to_celsius(api_response['main']['temp']),
                                       max_temp=to_celsius(api_response['main']['temp_max']),
                                       min_temp=to_celsius(api_response['main']['temp_min']),
                                       description=api_response['weather'][0]['main'],
                                       icon=icon_to_url(api_response['weather'][0]['icon']),
                                       humidity=api_response['main']['humidity'],
                                       pressure=api_response['main']['pressure'])
        except Exception as e:
            return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response.to_json())


@api_view(['GET'])
def get_multiple_days_weather(request, num_of_days, city_name):
    if request.method == 'GET':
        response = []
        if num_of_days >= 16 or num_of_days < 1:
            error_message = "Invalid number of days. Should be in between [1, 16]"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        try:
            api_response = requests.get(OPEN_FORECAST_API_URL.format(city_name, num_of_days))
            api_response = api_response.json()

            for result in api_response['list']:
                response.append(WeatherResponse(max_temp=to_celsius(result['temp']['max']),
                                                min_temp=to_celsius(result['temp']['min']),
                                                description=result['weather'][0]['main'],
                                                icon=icon_to_url(result['weather'][0]['icon']),
                                                humidity=result['humidity'],
                                                pressure=result['pressure']).to_json())
        except Exception as e:
            return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response)
