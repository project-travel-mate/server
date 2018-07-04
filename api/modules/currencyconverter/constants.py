"""
The Free Currency Converter API
Reference Docs: https://free.currencyconverterapi.com/
"""


import os
from api.modules.currencyconverter.currencycon_item  import CurrencyItem

# source= CurrencyItem.to_json()["source"]
# target= CurrencyItem.to_json()["target"]

CURRENCY_CONVERTER_API_URL = 'https://www.currencyconverterapi.com/api/v5/convert?q={}&compact=ultra'