from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from email.utils import parseaddr
import string


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    """
    Adds a new user to database
    Note: client's email is stored as username in database (NO explicit difference in email and username)
    :param request: contains first name, last name, email Id (username) and password
    :return:
    """
    firstname = request.POST.get('firstname', None)
    lastname = request.POST.get('lastname', None)
    username = parseaddr(request.POST.get('email', None))[1]
    password = request.POST.get('password', None)

    if not firstname or not lastname or not username or not password:
        # incorrect request received
        error_message = "Missing parameters in request. Send firstname, lastname, email, password"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    if '@' not in username:
        error_message = "Invalid email Id"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    if not test_password(password):
        error_message = "Invalid Password"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=username)
        error_message = "Email Id already exists"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        user = User.objects.create_user(username, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.is_superuser = False
        user.is_staff = False
        user.save()
    except Exception as e:
        error_message = str(e)
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    success_message = "Successfully registered"
    return Response(success_message, status=status.HTTP_201_CREATED)


def long_enough(pw):
    # Password must be at least length 8
    return len(pw) >= 8


def has_letter(pw):
    # Password must contain a lowercase letter
    return any(character.isalpha() for character in pw)


def has_numeric(pw):
    # Password must contain a digit
    return len(set(string.digits).intersection(pw)) > 0


def has_special(pw):
    # Password must contain a special character
    return len(set(string.punctuation).intersection(pw)) > 0


def test_password(pw, tests=[long_enough, has_letter, has_numeric, has_special]):
    for test in tests:
        if not test(pw):
            return False
    return True
