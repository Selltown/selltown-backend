from rest_framework.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger(__name__)


def change_user_password(*, user, current_password, new_password):
    if not user.check_password(current_password):
        logger.warning(
            f"Current password provided by user with phone number: {user.phone_number} when changing password is incorrect."
        )
        raise AuthenticationFailed("Current password is incorrect.")

    user.set_password(new_password)
    user.save(update_fields=["password"])

    logger.info(
        f"User with phone number: {user.phone_number} has successfully changed their password."
    )

    return user
