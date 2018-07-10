import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.modules.currency.constants import CURRENCY_CONVERTER_API_URL
from api.modules.currency.currency_item import CurrencyItem


@api_view(['GET'])
def get_currency_exchange_rate(request, source_currency_code, target_currency_code):
    """
    Return currency conversion rate using source and target currency codes
    :param request:
    :param source_currency_code:
    :param target_currency_code:
    :return: 503 if Free Currency Converter api fails
    :return: 200 successful
    """
    query = "{0}_{1}".format(source_currency_code, target_currency_code)
    try:
        api_response = requests.get(CURRENCY_CONVERTER_API_URL.format(query))
        api_response_json = api_response.json()
        if not api_response.ok:
            error_message = "Missing parameters in the api response"
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response = CurrencyItem(source=api_response_json["results"][query]["fr"],
                                target=api_response_json["results"][query]["to"],
                                result=api_response_json["results"][query]["val"])

    except Exception as e:
        exception_message = "Incorrect currency codes {}".format(query)
        return Response(exception_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(response.to_json())
