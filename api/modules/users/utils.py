from random import randint

LENGTH_OF_FORGET_PASSWORD_CODE = 4


def generate_random_code(n=LENGTH_OF_FORGET_PASSWORD_CODE):
    """
    Generate 'N' digit numeric random code for forgot password
    """
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)
