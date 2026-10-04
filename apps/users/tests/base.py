from rest_framework.test import APITestCase
from ...crafts.models import Craft
from ...locations.models import Location


class BaseAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.craft = Craft.objects.create(craft_name="Plumber")
        cls.location = Location.objects.create()

        cls.artisan_data = {
            "name": "test artisan",
            "phone_number": "+233554089218",
            "password": "lovesogreat",
            "craft": cls.craft.id,
            "location": {
                "place_id": "ty789",
                "name": "Amasaman North",
                "city": "Accra",
                "full_address": "Amasaman",
                "region": "Greater Accra",
                "longitude": "12345",
                "latitude": "5678",
            },
            "role": "artisan",
        }

        cls.customer_data = {
            "name": "test customer",
            "phone_number": "+233554089218",
            "password": "lovesogreat",
            "role": "customer",
        }
