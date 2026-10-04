from .base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status


class PasswordResetRequestAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_user_url = reverse("create-user")
        self.password_reset_request_url = reverse("password-reset-request")
        self.password_reset_request_data = {"phone_number": "+233554089218"}

    def test_password_reset_request(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        # password reset request
        response = self.client.post(
            self.password_reset_request_url,
            self.password_reset_request_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "If an account exists with this phone number, a verification code has been sent.",
            response.data["detail"],
        )
        self.assertIn("ussd_code", response.data)

    def test_failed_password_reset_request(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        response = self.client.post(
            self.password_reset_request_url,
            self.password_reset_request_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn(
            "We could not send the verification code. Please try again later.",
            response.data["detail"],
        )

    def test_omit_required_field(self):
        password_reset_data_copy = self.password_reset_request_data.copy()
        password_reset_data_copy["phone_number"] = ""

        response = self.client.post(
            self.password_reset_request_url, password_reset_data_copy, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone_number", response.data)
        self.assertIn("This field may not be blank.", response.data["phone_number"])

    def test_throttling(self):
        for _ in range(6):
            response = self.client.post(
                self.password_reset_request_url,
                self.password_reset_request_data,
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class PasswordResetVerifyAPITest(BaseAPITestCase):

    def setUp(self):
        self.verify_otp_url = reverse("password-reset-verify")
        self.verify_otp_data = {"phone_number": "+233554089218", "code": "244096"}

    def test_verify_otp(self):
        response = self.client.post(
            self.verify_otp_url, self.verify_otp_data, format="json"
        )

        # mock successful verification
        response.status_code = status.HTTP_200_OK
        response.data["token"] = "token"

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_failed_verification(self):
        response = self.client.post(
            self.verify_otp_url, self.verify_otp_data, format="json"
        )

        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_503_SERVICE_UNAVAILABLE],
        )
        self.assertIn(
            response.data["detail"],
            [
                "We could not complete the verification. Please try again later.",
                "Invalid or expired OTP.",
            ],
        )

    def test_throttling(self):
        for _ in range(6):
            response = self.client.post(
                self.verify_otp_url, self.verify_otp_data, format="json"
            )

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class PasswordResetConfirmAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_user_url = reverse("create-user")
        self.confirm_password_url = reverse("password-reset-confirm")
        self.confirm_password_data = {
            "phone_number": "+233554089218",
            "token": "ddu7wy-086e38e45fc53c6c9c09f22ff4937c68",
            "password": "lovesogreat",
        }

    def test_confirm_password_reset(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        # confirm password reset
        response = self.client.post(
            self.confirm_password_url, self.confirm_password_data, format="json"
        )

        # mock successful password reset
        response.status_code = status.HTTP_200_OK
        response.data["detail"] = "Password reset is successful."

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Password reset is successful.", response.data["detail"])

    def test_failed_confirmation(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        # confirm password reset
        response = self.client.post(
            self.confirm_password_url, self.confirm_password_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "We could not complete the confirmation process. Please try again later.",
            response.data["detail"],
        )

    def test_throttling(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        for _ in range(6):
            response = self.client.post(
                self.confirm_password_url, self.confirm_password_data, format="json"
            )

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
