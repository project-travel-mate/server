from django.test import TestCase
from api.views import test_password

################################################################


def data_provider(fn_data_provider):
    def test_decorator(fn):
        def repl(self, *args):
            for i in fn_data_provider():
                try:
                    fn(self, *i)
                except AssertionError:
                    print("Assertion error caught with data set ", i)
                    raise
        return repl
    return test_decorator

################################################################


class test_pasword(TestCase):

    DataProvider = lambda: (
        ("abcde", False),
        ("12345678", False),
        ("1a2b3c4e", False),
        ('1a2b3c4!', True),
    )

    @data_provider(DataProvider)
    def test_password(self, password, expected):
        result = test_password(password)
        self.assertEqual(result, expected)
