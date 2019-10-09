from random import randint

from django.utils import timezone

LENGTH_OF_FORGET_PASSWORD_CODE = 4
NUMBER_OF_SECONDS = 86400


def generate_random_code(n=LENGTH_OF_FORGET_PASSWORD_CODE):
    """
    Generate 'N' digit numeric random code for forgot password
    """
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def is_password_verification_code_valid(code):
    """
    Verify if the password verification code is expired or not
    :param code:
    :return: True if the code was generated within 24 hours
    :return: False is the code was expired
    """
    created_at = code.created
    current_time = timezone.now()
    delta = current_time - created_at
    return delta.total_seconds() < NUMBER_OF_SECONDS
