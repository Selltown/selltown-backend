from rest_framework import generics
from ..serializers.password_reset import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
)
from ..throttles import PasswordResetRequestThrottle, PasswordResetVerifyThrottle
from ..services.otp.arkesel import send_otp, ArkeselError, verify_otp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
import logging
from ..services.password_reset import create_reset_token

logger = logging.getLogger(__name__)


class PasswordResetRequestAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    throttle_classes = [PasswordResetRequestThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            data = send_otp(serializer.validated_data["phone_number"])
            logger.info("Verification code has been sent to user's phone number.")
            return Response(
                {
                    "detail": "If an account exists with this phone number, a verification code has been sent.",
                    "ussd_code": data.get("ussd_code"),
                },
                status=status.HTTP_200_OK,
            )

        except ArkeselError, NotFound:
            logger.exception("Failed to send verification code to user's phone number.")
            return Response(
                {
                    "detail": "We could not send the verification code. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class PasswordResetVerifyAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetVerifySerializer
    throttle_classes = [PasswordResetVerifyThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            verified = verify_otp(
                phone_number=serializer.validated_data["phone_number"],
                code=serializer.validated_data["code"],
            )

        except ArkeselError:
            return Response(
                {
                    "detail": "We could not complete the verification. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if not verified:
            return Response(
                {"detail": "Invalid or expired OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = create_reset_token(serializer.validated_data["phone_number"])

        return Response({"token": token}, status=status.HTTP_200_OK)
