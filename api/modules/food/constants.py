"""
This has used the Zomato Api
For more information look into https://developers.zomato.com/api
Environment variable for API to be set
"""
import os
ORIGINAL_ZOMATO_API = ""
ZOMATO_API_KEY = os.environ.get("ZOMATO_API", ORIGINAL_ZOMATO_API)
BASE_URL = "https://developers.zomato.com/api/v2.1/"
LIST = "geocode?lat={0}&lon={1}"
RESTAURANT = "restaurant?res_id={0}"
USER_AGENT = "curl/7.43.0"
ACCEPT = "application/json"
