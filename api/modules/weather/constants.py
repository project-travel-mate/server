"""
Uses the OpenWeatherMap API (Reference: https://openweathermap.org)

Current city weather API reference doc: https://openweathermap.org/current
Weather forecast API reference doc: https://openweathermap.org/forecast16
"""
import os

# should only be used for development purposes
DEFAULT_OPEN_WEATHER_API_KEY = "1aa19f7dca713b11c29ec2cda827994c"
OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API", DEFAULT_OPEN_WEATHER_API_KEY)

OPEN_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&APPID=" + OPEN_WEATHER_API_KEY
OPEN_FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/forecast/daily?q={0}&cnt={1}&APPID=" + \
                        OPEN_WEATHER_API_KEY
