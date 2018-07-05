"""
This has used the Zomato Api
For more information look into https://developers.zomato.com/api
"""
import os

ORIGINAL_ZOMATO_API = "9a656813579b698902619a05684d39c6"
ZOMATO_API_KEY = os.environ.get("ZOMATO_API", ORIGINAL_ZOMATO_API)
BASE_URL = "https://developers.zomato.com/api/v2.1/geocode?lat={0}&lon={1}"
USER_AGENT: "curl/7.43.0"
ACCEPT:  "application/json"
