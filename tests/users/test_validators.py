from django.test import TestCase
from api.modules.users.validators import validate_password, validate_email


class TestValidators(TestCase):
    def test_validate_password(self):
        data_provider = [
            {"password": "abcde", "result": False},
            {"password": "12345678", "result": False},
            {"password": "1a2b3c4e", "result": False},
            {"password": '1a2b3c4!', "result": True},
        ]
        for data in data_provider:
            result = validate_password(data['password'])
            self.assertEqual(result, data['result'])

    def test_validate_email(self):
        data_provider = [
            {"email": "1a2b3c4e", "result": False},
            {"email": 'test@test.com', "result": True},
        ]
        for data in data_provider:
            result = validate_email(data['email'])
            self.assertEqual(result, data['result'])
