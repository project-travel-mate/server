import requests
import requests_cache
from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import City
from api.modules.weather.constants import OPEN_WEATHER_API_URL, OPEN_FORECAST_API_URL
from api.modules.weather.utils import to_celsius, icon_to_url
from api.modules.weather.weather_response import WeatherResponse

hour_difference = timedelta(hours=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_city_weather(request, city_id):
    """
    Return current city weather using city name
    :param request:
    :param city_id:
    :return: 404 if Invalid City ID is passed
    :return: 503 if OpenWeatherMap api fails
    :return: 200 successful
    """
    try:
        city = City.objects.get(pk=city_id)
    except City.DoesNotExist:
        error_message = "Invalid City ID"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)

    try:
        api_response = requests.get(OPEN_WEATHER_API_URL.format(city.latitude, city.longitude))
        api_response_json = api_response.json()
        if not api_response.ok:
            error_message = api_response_json['message']
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response = WeatherResponse(temp=to_celsius(api_response_json['main']['temp']),
                                   max_temp=to_celsius(api_response_json['main']['temp_max']),
                                   min_temp=to_celsius(api_response_json['main']['temp_min']),
                                   code=api_response_json['weather'][0]['id'],
                                   condensed=api_response_json['weather'][0]['main'],
                                   description=api_response_json['weather'][0]['description'],
                                   icon=icon_to_url(api_response_json['weather'][0]['icon']),
                                   humidity=api_response_json['main']['humidity'],
                                   pressure=api_response_json['main']['pressure'])
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response.to_json())


@api_view(['GET'])
def get_multiple_days_weather(request, num_of_days, city_name):
    """
    Returns 'num_of_days' forecast for given city using 'city_name'
    :param request:
    :param num_of_days:
    :param city_name:
    :return: 400 if number of days ar not in [1,16] range
    :return: 503 if OpenWeatherMap api fails
    :return: 200 successful
    """
    response = []
    if num_of_days >= 16 or num_of_days < 1:
        error_message = "Invalid number of days. Should be in between [1, 16]"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    try:
        api_response = requests.get(OPEN_FORECAST_API_URL.format(city_name, num_of_days))
        api_response_json = api_response.json()
        if not api_response.ok:
            error_message = api_response_json['message']
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        for result in api_response_json['list']:
            response.append(WeatherResponse(max_temp=to_celsius(result['temp']['max']),
                                            min_temp=to_celsius(result['temp']['min']),
                                            code=result['weather'][0]['id'],
                                            condensed=result['weather'][0]['main'],
                                            description=result['weather'][0]['description'],
                                            icon=icon_to_url(result['weather'][0]['icon']),
                                            humidity=result['humidity'],
                                            pressure=result['pressure']).to_json())
    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response)
