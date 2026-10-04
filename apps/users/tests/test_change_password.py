from .base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status
from ...users.models.user import CustomUser


class ChangePasswordAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_user_url = reverse("create-user")
        self.change_password_url = reverse("change-password")
        self.change_password_data = {
            "current_password": "lovesogreat",
            "new_password": "lovesogreat",
        }

    def authenticate_user(self, user):
        self.client.force_authenticate(user=user)

    def test_change_password(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        # authenticate user
        user = CustomUser.objects.get(phone_number=self.artisan_data["phone_number"])
        self.authenticate_user(user)

        # change password
        response = self.client.post(
            self.change_password_url, self.change_password_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Password changed successfully.", response.data["detail"])

    def test_failed_password_change(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        # authenticate user
        user = CustomUser.objects.get(phone_number=self.artisan_data["phone_number"])
        self.authenticate_user(user)

        # change password
        invalid_data = {
            "current_password": "mypassword",
            "new_password": "lovesogreat",
        }
        response = self.client.post(
            self.change_password_url, invalid_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Current password is incorrect.", response.data["detail"])

    def test_throttling(self):
        # create user
        self.client.post(self.create_user_url, self.artisan_data, format="json")

        # authenticate user
        user = CustomUser.objects.get(phone_number=self.artisan_data["phone_number"])
        self.authenticate_user(user)

        # change password
        for _ in range(6):
            response = self.client.post(
                self.change_password_url,
                self.change_password_data,
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
