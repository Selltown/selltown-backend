from rest_framework import generics
from ..serializers.password_reset import PasswordResetRequestSerializer
from ..throttles import PasswordResetRequestThrottle
from ..services.otp.arkesel import send_otp, ArkeselError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
import logging

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
