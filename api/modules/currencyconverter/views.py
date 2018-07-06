import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.modules.currencyconverter.constants import CURRENCY_CONVERTER_API_URL
from api.modules.currencyconverter.currencycon_item import CurrencyItem


@api_view(['GET'])
def get_currency_exchange_rate(request, query):

    try:
        api_response = requests.get(CURRENCY_CONVERTER_API_URL.format(query))
        api_response_json = api_response.json()
        if not api_response.ok:
            error_message = "Missing parameters in request"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        response = CurrencyItem(source=api_response_json["results"][query]["fr"],
                                target=api_response_json["results"][query]["to"],
                                result=api_response_json["results"][query]["val"])

    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response.to_json())
