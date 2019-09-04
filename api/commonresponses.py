from rest_framework import status
from rest_framework.response import Response

DOWNSTREAM_ERROR_RESPONSE = Response("Downstream service failed.", status=status.HTTP_503_SERVICE_UNAVAILABLE)
