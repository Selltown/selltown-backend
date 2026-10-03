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


def validate_reset_token(*, phone_number, token):
    user = CustomUser.objects.get(phone_number=phone_number)
    return default_token_generator.check_token(user, token)


def reset_user_password(*, phone_number, password):
    user = CustomUser.objects.get(phone_number=phone_number)
    user.set_password(password)
    user.save(update_fields=["password"])
    logger.info(
        f"User with phone number: {phone_number} has successfully reset their password."
    )
    return user
