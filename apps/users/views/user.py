from ..models.user import CustomUser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from ..serializers.user import CreateUserSerializer
from ..throttles import RegistrationThrottle
from ..services.otp.arkesel import send_otp, ArkeselError
from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    throttle_classes = [RegistrationThrottle]
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user(**serializer.validated_data)

        try:
            data = send_otp(user.phone_number)
            return Response(
                {
                    "detail": "OTP sent successfully.",
                    "ussd_code": data.get("ussd_code"),
                },
                status=status.HTTP_200_OK,
            )

        except ArkeselError, NotFound:
            return Response(
                {
                    "detail": "We could not send the verification code. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
