"""
    Use Places API to access locations using longitude and latitude
"""
import os

PLACES_API_BASE_URL = 'https://places.cit.api.here.com/places/v1/autosuggest?'
PLACES_API_APP_ID = os.environ.get("PLACES_API_APP_ID", "")
PLACES_API_APP_CODE = os.environ.get("PLACES_API_APP_CODE", "")

PLACES_SEARCH_API_URL = PLACES_API_BASE_URL + 'at={latitude},{longitude}&q={place_keyword}' + '&app_id=' + \
                        PLACES_API_APP_ID + '&app_code=' + PLACES_API_APP_CODE
