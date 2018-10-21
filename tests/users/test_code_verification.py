from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import PasswordVerification
from api.modules.users.utils import generate_random_code


class TestVerificationCode(APITestCase):
    def test_confirm_verification_code(self):
        """
        Ensure verification code is confirm and user profile is
        set to is_verified.
        """
        user = User.objects.create_user('john', 'johnpassword')
        code = generate_random_code(6)
        PasswordVerification.objects.create(
            user=user,
            code=code,
            created=timezone.now()
        )

        url_invalid = reverse('confirm-verification-code',
                              kwargs={'verification_code': "invalid-code"})
        response = self.client.get(url_invalid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'"Unable to confirm verification code"')
        self.assertEqual(User.objects.get().profile.is_verified, False)

        url_valid = reverse('confirm-verification-code',
                            kwargs={'verification_code': code})
        response = self.client.get(url_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().profile.is_verified, True)
