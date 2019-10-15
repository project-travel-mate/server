from email.utils import parseaddr


def _long_enough(pw):
    """
    Password must be at least length 8
    :param pw: password string
    :return: boolean
    """
    return len(pw) >= 8


def _has_at(email):
    """
    Email must contain '@'
    :param email:
    :return: boolean
    """
    return '@' in email


def _is_email(email):
    """
    Email must contain '@'
    :param email:
    :return: boolean
    """
    return '@' in parseaddr(email)[1]


def validate_password(password, tests=None):
    """
    Validates password
    :param password:
    :param tests:
    :return: boolean
    """
    if not tests:
        tests = [_long_enough]

    for test in tests:
        if not test(password):
            return False
    return True


def validate_email(email, tests=None):
    """
    Validates email address
    :param email:
    :param tests:
    :return: boolean
    """
    if not tests:
        tests = [_has_at]
        
    if not tests:
        tests = [_is_email]

    for test in tests:
        if not test(email):
            return False
    return True
