import requests
import requests_cache
from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.modules.shopping.constants import EBAY_API_URL
from api.modules.shopping.shopping_item import ShoppingItem

day_difference = timedelta(days=1)
requests_cache.install_cache(expire_after=day_difference)


@api_view(['GET'])
def get_shopping_info(request, query):
    """
    Returns a list of responses from
    :param request:
    :param query:
    :return: 503 Ebay request fails
    :return: 200 successful
    """
    try:
        api_response = requests.get(EBAY_API_URL.format(query))
        api_response_json = api_response.json()
        if not api_response.ok:
            error_message = api_response_json['errorMessage'][0]['error'][0]['message'][0]
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        #  if ebay api returns empty response with no items
        if api_response_json['findItemsAdvancedResponse'][0]['searchResult'][0]['@count'] == '0':
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        response = []
        for item in api_response_json['findItemsAdvancedResponse'][0]['searchResult'][0]['item']:
            response.append(ShoppingItem(
                name=item['title'][0],
                url=item['viewItemURL'][0],
                image=item['galleryURL'][0],
                value=item['sellingStatus'][0]['currentPrice'][0]['__value__'],
                currency=item['sellingStatus'][0]['currentPrice'][0]['@currencyId'],
            ).to_json())

    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response)
