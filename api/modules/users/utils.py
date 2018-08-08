import random
import string


def generate_random_code():
    """
    Generate 6 digit alphanumeric random code for forgot password
    """
    LENGTH_OF_CODE = 6
    code = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(LENGTH_OF_CODE)
    )
    return code
