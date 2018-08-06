"""
This has used the Zomato Api
For more information look into https://developers.zomato.com/api
Environment variable for API to be set
"""
import os

ZOMATO_API_KEY = os.environ.get("ZOMATO_API", "")
BASE_API_URL = "https://developers.zomato.com/api/v2.1/"

GET_ALL_RESTAURANTS_API_URL = BASE_API_URL + "geocode?lat={0}&lon={1}"
GET_RESTAURANT_API_URL = BASE_API_URL + "restaurant?res_id={0}"

FOOD_API_REQUEST_HEADERS = {
    "User-agent": "curl/7.43.0",
    "Accept": "application/json",
    "user_key": ZOMATO_API_KEY
}
