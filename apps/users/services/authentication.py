from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from ...users.models import CustomUser

logger = logging.getLogger(__name__)


def authenticate_user(*, phone_number, password):
    user = authenticate(phone_number=phone_number, password=password)

    if user is None:
        logger.warning(f"Failed authentication for phone number: {phone_number}")
        raise AuthenticationFailed("Invalid phone number or password.")

    if not user.is_phone_verified:
        logger.warning(f"Unverified phone attempted authentication: {phone_number}")
        raise AuthenticationFailed("Phone number has not been verified.")

    access_token, refresh_token = generate_tokens(user)

    logger.info(f"User authentication successful for phone number: {phone_number}")

    return access_token, refresh_token, user


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    logger.info(f"Generated tokens for user with phone number: {user.phone_number}")
    return refresh.access_token, refresh


def generate_tokens_for_user(phone_number):
    user = CustomUser.objects.get(phone_number=phone_number)
    access_token, refresh_token = generate_tokens(user)
    return access_token, refresh_token, user
