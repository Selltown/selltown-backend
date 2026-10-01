import logging
from ..serializers.user import ReadArtisanSerializer, ReadCustomerSerializer

logger = logging.getLogger(__name__)


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
