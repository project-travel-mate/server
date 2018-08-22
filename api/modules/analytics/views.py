from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User


@api_view(['GET'])
def get_total_users(request):
    """
    Returns number of users
    :param request:
    :return: 200 successful
    """
    number_of_users = User.objects.count()
    res = {
        'total_users': number_of_users,
    }
    return Response(res, status=status.HTTP_200_OK)
