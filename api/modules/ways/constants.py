"""
Use Google Maps API to get ways to reach for a given source and destination
Reference:
Place search API: https://developers.google.com/places/web-service/search
Place autocomplete API: https://developers.google.com/places/web-service/search
Distance Matrix API: https://developers.google.com/maps/documentation/distance-matrix/intro
"""

import os

PLACE_AUTOCOMPLETE_API_BASE_URL = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={}&key='
DISTANCE_MATRIX_API_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations' \
                               '={}&mode={walk_or_drive}&key='
PLACE_SEARCH_API_BASE_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&type={}&key='
PLACE_DETAIL_API_BASIC_URL = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&fields=address_' \
                             'component&key='
PLACE_API_KEY = os.environ.get('GOOGLE_MAPS_PLACE_API_KEY', None)
DISTANCE_MATRIX_API_KEY = os.environ.get('GOOGLE_MAPS_DISTANCE_MATRIX_API_KEY', None)
PLACE_AUTOCOMPLETE_API_URL = PLACE_AUTOCOMPLETE_API_BASE_URL
PLACE_SEARCH_API_URL = PLACE_SEARCH_API_BASE_URL
PLACE_DETAIL_API_URL = PLACE_DETAIL_API_BASIC_URL
DISTANCE_MATRIX_API_URL = DISTANCE_MATRIX_API_BASE_URL


if PLACE_API_KEY:
    PLACE_AUTOCOMPLETE_API_URL = PLACE_AUTOCOMPLETE_API_BASE_URL + PLACE_API_KEY
    PLACE_SEARCH_API_URL = PLACE_SEARCH_API_BASE_URL + PLACE_API_KEY
    PLACE_DETAIL_API_URL = PLACE_DETAIL_API_BASIC_URL + PLACE_API_KEY
if DISTANCE_MATRIX_API_KEY:
    DISTANCE_MATRIX_API_URL = DISTANCE_MATRIX_API_BASE_URL + DISTANCE_MATRIX_API_KEY
