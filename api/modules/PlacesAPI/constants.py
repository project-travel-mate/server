"""
    Use Places API to access locations using longitude and latitude
"""
import os

BASE_URL = 	'https://places.cit.api.here.com/places/v1/autosuggest?'
APP_ID = os.environ.get("YOUR_APP_ID", "")
APP_CODE = os.environ.get("YOUR_APP_CODE", "")

PLACES_API_SEARCH = BASE_URL + 'at={latitude},{longitude}&q={place_keyword}'+ '&app_id=' + APP_ID + '&app_code=' + \
                    APP_CODE
