"""
Use Places API to access locations using longitude and latitude
Reference: https://developer.here.com/documentation/places/topics_api/resource-explore.html
Categories Reference: https://developer.here.com/documentation/places/topics_api/resource-explore.html
"""
import os

PLACES_API_BASE_URL = 'https://places.api.here.com/places/v1/discover/explore?'
PLACES_API_APP_ID = os.environ.get("PLACES_API_APP_ID", None)
PLACES_API_APP_CODE = os.environ.get("PLACES_API_APP_CODE", None)

PLACES_SEARCH_API_URL = PLACES_API_BASE_URL + 'at={latitude},{longitude}&cat={places_query}'

if PLACES_API_APP_ID and PLACES_API_APP_CODE:
    PLACES_SEARCH_API_URL += '&app_id=' + PLACES_API_APP_ID + '&app_code=' + PLACES_API_APP_CODE
