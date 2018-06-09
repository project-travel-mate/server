from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth.models import User
import requests

from api.modules.city import view as city

@api_view(['POST'])
@permission_classes((AllowAny, ))
def sign_up(request):
    """
    Adds a new user to Database
    :param request:
    :return:
    """

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']

    try:
        user = User.objects.get(username=username)
        return Response("Username already exists", status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=email)
            return Response("Email already exists", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user=User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.is_superuser=False
            user.is_staff=False
            user.save()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes((AllowAny, ))
def sign_in(request):
    """
    Signs in user
    :param request:
    :return:
    """
    username = request.POST['username']
    password = request.POST['password']

    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            post_data = {'username': username, 'password': password}
            response = requests.post('http://localhost:8000/api/obtain-auth-token/', data=post_data)
            content = response.content
            return Response(content)
        else:
            return Response("Incorrect Password.", status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response("User does not exist. Kindly Sign Up.", status=status.HTTP_400_BAD_REQUEST)