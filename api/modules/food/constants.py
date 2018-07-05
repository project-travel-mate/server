"""
This has used the Zomato Api
For more information look into https://developers.zomato.com/api
"""
ZOMATO_API = "9a656813579b698902619a05684d39c6"
BASE_URL = "https://developers.zomato.com/api/v2.1/geocode?"
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": ZOMATO_API}
