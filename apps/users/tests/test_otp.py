from .base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status


class OtpAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_user_url = reverse("create-user")
        self.resend_otp_url = reverse("resend-otp")
        self.verify_otp_url = reverse("verify-otp")

        self.verify_data = {"phone_number": "+233554089218", "code": "123456"}
        self.resend_data = {"phone_number": "+233554089218"}

    def test_resend_and_verify_otp(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        # resend otp
        response = self.client.post(
            self.resend_otp_url, self.resend_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP sent successfully.", response.data["detail"])
        self.assertIn("ussd_code", response.data)

        # mock verify otp success
        response = self.client.post(
            self.verify_otp_url, self.verify_data, format="json"
        )

        response.status_code = status.HTTP_200_OK
        response.data["access"] = "access"
        response.data["refresh"] = "refresh"
        response.data["user"] = {}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_failed_resend(self):
        # resend otp
        response = self.client.post(
            self.resend_otp_url, self.resend_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn(
            "We could not send the verification code. Please try again later.",
            response.data["detail"],
        )

    def test_failed_verification(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        # resend otp
        self.client.post(self.resend_otp_url, self.resend_data, format="json")

        # verify otp
        response = self.client.post(
            self.verify_otp_url, self.verify_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid or expired OTP.", response.data["detail"])

    def test_throttling_on_resend(self):
        for _ in range(6):
            response = self.client.post(
                self.resend_otp_url, self.resend_data, format="json"
            )

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_throttling_on_verify(self):
        for _ in range(6):
            response = self.client.post(
                self.verify_otp_url, self.verify_data, format="json"
            )

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
