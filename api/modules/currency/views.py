import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.modules.currency.constants import CURRENCY_CONVERTER_API_URL, CURRENCY_VALUE_DATE_API_URL
from api.modules.currency.currency_item import CurrencyItem, CurrencyDate
import datetime
from datetime import timedelta


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


@api_view(['GET'])
def get_all_currency_exchange_rate(request, start_date, end_date, source_currency_code, target_currency_code):
    """
    Return currency exchange rates list between 2 dates
    :param request:
    :param start date:
    :param end date:
    :param source_currency_code:
    :param target_currency_code:
    :return 400 response if dates are incorrect
    :return: 503 if Free Currency Converter api fails
    :return: 200 successful
    """
    currency_list = []
    y_start = start_date.split('-')[0]
    m_start = start_date.split('-')[1]
    d_start = start_date.split('-')[2]
    start = datetime.datetime.strptime(y_start+m_start+d_start, '%Y%m%d').date()
    y_end = end_date.split('-')[0]
    m_end = end_date.split('-')[1]
    d_end = end_date.split('-')[2]
    end = datetime.datetime.strptime(y_end+m_end+d_end, '%Y%m%d').date()
    if end < start:
        error_message = "End Date is before Start Date"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    try:
        api_response_start = requests.get(CURRENCY_VALUE_DATE_API_URL.format(
            start_date, source_currency_code, target_currency_code))
        api_response_end = requests.get(CURRENCY_VALUE_DATE_API_URL.format(
            end_date, source_currency_code, target_currency_code))
        if not api_response_start.ok or not api_response_end.ok:
            error_message = "Incorrect parameters please check dates"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        delta = end - start
        for day in range(delta.days + 1):
            actual_date = str(start + timedelta(day))
            response = requests.get(CURRENCY_VALUE_DATE_API_URL.format(
                actual_date, source_currency_code, target_currency_code))
            currency_value = response.json()
            currency_list.append(CurrencyDate(value=str(currency_value)).to_json())

    except Exception as e:
        return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(currency_list)
