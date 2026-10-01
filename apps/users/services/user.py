from django.db import transaction
from ...users.models.customer import CustomerProfile
from ...users.models.user import CustomUser
from ...users.models.artisan import ArtisanProfile
from ...locations.models import Location
import logging

logger = logging.getLogger(__name__)


@transaction.atomic
def create_user(*, phone_number, name, password, role, craft=None, location=None):
    user = CustomUser.objects.create_user(
        phone_number=phone_number,
        name=name,
        password=password,
    )

    if role == "artisan":
        location = Location.objects.create(**location)
        logger.info(f"Location ({location.city}) ({location.full_address}) created")

        ArtisanProfile.objects.create(
            user=user,
            craft=craft,
            location=location,
        )
        logger.info(
            f"Artisan profile has been created for user with phone number: {phone_number}"
        )
    else:
        CustomerProfile.objects.create(
            user=user,
        )
        logger.info(
            f"Customer profile has been created for user with phone number: {phone_number}"
        )

    return user
