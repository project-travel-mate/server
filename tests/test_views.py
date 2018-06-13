from django.test import TestCase
from api.views import validatePassword


class test_views(TestCase):

    def test_validatePassword(self):
        DataProvider = [
            {"password": "abcde", "result": False},
            {"password": "12345678", "result": False},
            {"password": "1a2b3c4e", "result": False},
            {"password": '1a2b3c4!', "result": True},
        ]
        for data in DataProvider:
            result = validatePassword(data['password'])
            self.assertEqual(result, data['result'])
