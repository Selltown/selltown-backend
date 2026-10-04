from .base import BaseAPITestCase
from django.urls import reverse
from ...users.models.user import CustomUser
from rest_framework import status


class LoginAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_user_url = reverse("create-user")
        self.login_url = reverse("login")
        self.login_data = {"phone_number": "+233554089218", "password": "lovesogreat"}

    def test_login(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        user = CustomUser.objects.get(phone_number="+233554089218")
        user.is_phone_verified = True
        user.save(update_fields=["is_phone_verified"])

        # login
        response = self.client.post(self.login_url, self.login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
        self.assertIn("location", response.data["user"])
        self.assertIn("name", response.data["user"]["location"])

    def test_omit_required_field(self):
        login_data_copy = self.login_data.copy()
        login_data_copy["phone_number"] = ""

        response = self.client.post(self.login_url, login_data_copy, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone_number", response.data)
        self.assertIn("This field may not be blank.", response.data["phone_number"])

    def test_invalid_credentials(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        user = CustomUser.objects.get(phone_number="+233554089218")
        user.is_phone_verified = True
        user.save(update_fields=["is_phone_verified"])

        # login
        invalid_login_data = {"phone_number": "+233554089218", "password": "mypassword"}
        response = self.client.post(self.login_url, invalid_login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid phone number or password.", response.data["detail"])

    def test_throttling(self):
        for _ in range(6):
            response = self.client.post(self.login_url, self.login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
