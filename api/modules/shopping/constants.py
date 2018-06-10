"""
Uses ebay findItemsByKeywords API
Reference Docs: https://developer.ebay.com/devzone/finding/CallRef/findItemsByKeywords.html
"""
import os

# should only be used for development purposes
DEFAULT_EBAY_API_KEY = "NSIT22619-c5e7-41ee-9311-cbde5b60ca2"
EBAY_API_KEY = os.environ.get('EBAY_API_KEY', DEFAULT_EBAY_API_KEY)

EBAY_API_URL = 'http://svcs.ebay.com/services/search/FindingService/v1?' \
               'OPERATION-NAME=findItemsAdvanced&' \
               'RESPONSE-DATA-FORMAT=JSON&' \
               'REST-PAYLOAD&' \
               'keywords={0}&' \
               'SECURITY-APPNAME=' + EBAY_API_KEY
