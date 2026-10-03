from django.contrib.auth.tokens import default_token_generator
import logging
from ...users.models.user import CustomUser

logger = logging.getLogger(__name__)


def create_reset_token(phone_number):
    user = CustomUser.objects.get(phone_number=phone_number)
    logger.info(
        f"Password reset token has been created for user with phone number: {phone_number}"
    )
    return default_token_generator.make_token(user)
