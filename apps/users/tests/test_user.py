from .base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status
from ...users.models.artisan import ArtisanProfile
from ...users.models.customer import CustomerProfile
from ...users.models.user import CustomUser


class CreateUserAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_user_url = reverse("create-user")

    def test_create_artisan(self):
        response = self.client.post(
            self.create_user_url, self.artisan_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = CustomUser.objects.filter(phone_number="+233554089218")

        self.assertTrue(user.exists())
        self.assertTrue(ArtisanProfile.objects.filter(user=user.first()).exists())
        self.assertIn("OTP sent successfully.", response.data["detail"])
        self.assertIn("ussd_code", response.data)

    def test_create_customer(self):
        response = self.client.post(
            self.create_user_url, self.customer_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = CustomUser.objects.filter(phone_number="+233554089218")

        self.assertTrue(user.exists())
        self.assertTrue(CustomerProfile.objects.filter(user=user.first()).exists())
        self.assertIn("OTP sent successfully.", response.data["detail"])
        self.assertIn("ussd_code", response.data)

    def test_omit_required_field(self):
        user_data_copy = self.artisan_data.copy()
        user_data_copy["location"] = ""

        response = self.client.post(self.create_user_url, user_data_copy, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("location", response.data)
        self.assertIn("This field may not be blank.", response.data["location"])

    def test_omit_required_location_field(self):
        user_data_copy = self.artisan_data.copy()
        user_data_copy["location"]["name"] = ""

        response = self.client.post(self.create_user_url, user_data_copy, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data["name"])

    def test_throttling(self):
        for _ in range(6):
            response = self.client.post(
                self.create_user_url, self.artisan_data, format="json"
            )

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
