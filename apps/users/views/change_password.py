from rest_framework import generics
from ..serializers.change_password import ChangePasswordSerializer
from ..services.change_password import change_user_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import logging
from ..throttles import ChangePasswordThrottle
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    throttle_classes = [ChangePasswordThrottle]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            change_user_password(
                user=request.user,
                current_password=serializer.validated_data["current_password"],
                new_password=serializer.validated_data["new_password"],
            )

        except AuthenticationFailed:
            logger.exception("Failed to change user's password.")
            return Response(
                {"detail": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info("User's password was changed successfully.")
        return Response(
            {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
        )
