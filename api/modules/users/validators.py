import string


def _has_special(pw):
    """
    Password must contain a special character
    :param pw: password string
    :return: boolean
    """
    return len(set(string.punctuation).intersection(pw)) > 0


def _has_numeric(pw):
    """
    Password must contain a digit
    :param pw: password string
    :return: boolean
    """
    return len(set(string.digits).intersection(pw)) > 0


def _long_enough(pw):
    """
    Password must be at least length 8
    :param pw: password string
    :return: boolean
    """
    return len(pw) >= 8


def _has_letter(pw):
    """
    Password must contain a lowercase letter
    :param pw: password string
    :return: boolean
    """
    return any(character.isalpha() for character in pw)


def _has_at(email):
    """
    Email must contain '@'
    :param email:
    :return: boolean
    """
    return "@" in email


def validate_password(password, tests=None):
    """
    Validates password
    :param password:
    :param tests:
    :return: boolean
    """
    if not tests:
        tests = [_long_enough, _has_letter, _has_numeric, _has_special]

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

    for test in tests:
        if not test(email):
            return False
    return True
