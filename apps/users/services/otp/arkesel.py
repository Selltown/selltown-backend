from ...models.user import CustomUser
import logging
from rest_framework.exceptions import NotFound
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class ArkeselError(Exception):
    """Base exception for Arkesel API errors."""


def send_otp(phone_number):
    try:
        _ = CustomUser.objects.get(phone_number=phone_number)

    except CustomUser.DoesNotExist:
        logger.error("User with phone number %s does not exist.", phone_number)

        raise NotFound("User with this phone number does not exist.")

    try:
        response = requests.post(
            "https://sms.arkesel.com/api/otp/generate",
            headers={
                "api-key": settings.ARKESEL_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "expiry": 2,
                "length": 6,
                "medium": "sms",
                "message": "Your verification code is %otp_code%. It expires in 2 minutes.",
                "number": str(phone_number),
                "sender_id": settings.ARKESEL_SENDER_ID,
                "type": "numeric",
            },
            timeout=10,
        )

        response.raise_for_status()

    except requests.Timeout:
        logger.error("Arkesel request timed out when sending OTP.")
        raise ArkeselError("Arkesel request timed out.")

    except requests.RequestException:
        logger.error("Unable to communicate with Arkesel when sending OTP.")
        raise ArkeselError("Unable to communicate with Arkesel.")

    try:
        data = response.json()

    except ValueError:
        logger.error("Arkesel returned an invalid response when sending OTP.")
        raise ArkeselError("Arkesel returned an invalid response.")

    if data.get("code") != "1000":
        logger.error(
            f"Arkesel failed to send OTP: {data.get("message", "Failed to send OTP.")}"
        )
        raise ArkeselError(data.get("message", "Failed to send OTP."))

    logger.info(f"OTP sent successfully to phone number: {phone_number}")
    return data


def verify_otp(phone_number, code):
    try:
        response = requests.post(
            "https://sms.arkesel.com/api/otp/verify",
            headers={
                "api-key": settings.ARKESEL_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "number": str(phone_number),
                "code": code,
            },
            timeout=10,
        )

        response.raise_for_status()

    except requests.Timeout:
        logger.exception("Arkesel OTP verification request timed out.")
        raise ArkeselError("Arkesel request timed out.")

    except requests.RequestException:
        logger.exception("Unable to communicate with Arkesel during OTP verification.")
        raise ArkeselError("Unable to communicate with Arkesel.")

    try:
        data = response.json()

    except ValueError:
        logger.error("Arkesel returned an invalid response during OTP verification.")
        raise ArkeselError("Arkesel returned an invalid response.")

    if data.get("code") != "1100":
        logger.error("OTP verification failed.")
        return False

    logger.info("OTP verification was successful.")

    user = CustomUser.objects.get(phone_number=phone_number)
    user.is_phone_verified = True
    user.save(update_fields=["is_phone_verified"])

    logger.info("Phone number has been verified.")

    return True
