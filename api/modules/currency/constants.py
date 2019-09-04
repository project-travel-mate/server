import os

"""
The Free Currency Converter API
Reference Docs: https://free.currencyconverterapi.com/
"""

CURRENCY_CONVERTER_API_KEY = os.environ.get("CURRENCY_CONVERTER_API_KEY", '')

CURRENCY_CONVERTER_API_URL = 'https://free.currconv.com/api/v7/convert?q={}&compact=ultra&apiKey=' + \
                             CURRENCY_CONVERTER_API_KEY
CURRENCY_VALUE_DATE_API_URL = 'http://currencies.apps.grandtrunk.net/getrange/{0}/{1}/{2}/{3}'
