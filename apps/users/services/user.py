from ..serializers.user import ReadArtisanSerializer, ReadCustomerSerializer
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
        location_data = location

        location_obj, created = Location.objects.get_or_create(
            place_id=location_data["place_id"],
            defaults=location_data,
        )

        if created:
            logger.info(
                f"Location ({location_obj.city}) "
                f"({location_obj.full_address}) created"
            )
        else:
            logger.info(
                f"Existing location reused: "
                f"({location_obj.city}) ({location_obj.full_address})"
            )

        ArtisanProfile.objects.create(
            user=user,
            craft=craft,
            location=location_obj,
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


def get_user_data(user):
    if hasattr(user, "artisan_profile"):
        data = ReadArtisanSerializer(user).data
        data["role"] = "artisan"

        logger.info("User is an artisan.")

        return data

    elif hasattr(user, "customer_profile"):
        data = ReadCustomerSerializer(user).data
        data["role"] = "customer"

        logger.info("User is a customer.")

        return data
