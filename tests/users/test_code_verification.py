from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import PasswordVerification
from api.modules.users.enums import PasswordVerificationModeChoice
from api.modules.users.utils import generate_random_code


class TestVerificationCode(APITestCase):
    def test_confirm_verification_code(self):
        """
        Ensure verification code is confirm and user profile is
        set to is_verified.
        """
        username = "john"
        user = User.objects.create_user(username, 'johnpassword')
        code = generate_random_code(6)
        PasswordVerification.objects.create(
            user=user,
            code=code,
            mode=PasswordVerificationModeChoice.EMAIL_VERIFY,
        )

        self.client.force_authenticate(user=user)

        url_invalid = reverse('confirm-verification-code',
                              kwargs={'verification_code': "invalid-code"})
        response = self.client.get(url_invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'"Invalid code."')
        self.assertEqual(User.objects.get().profile.is_verified, False)

        url_valid = reverse('confirm-verification-code',
                            kwargs={'verification_code': code})
        response = self.client.get(url_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(username=username).profile.is_verified, True)
