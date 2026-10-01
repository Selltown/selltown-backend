from ..models.user import CustomUser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from ..serializers.user import CreateUserSerializer
from ..throttles import RegistrationThrottle
from ..services.otp.arkesel import send_otp, ArkeselError
from rest_framework import generics
from ..serializers.authentication import LoginSerializer
from ..throttles import LoginThrottle
from rest_framework.exceptions import AuthenticationFailed
from ..services.user import get_user_data
from ..services.authentication import authenticate_user


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


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [LoginThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            access_token, refresh_token, user = authenticate_user(
                phone_number=serializer.validated_data["phone_number"],
                password=serializer.validated_data["password"],
            )

        except AuthenticationFailed as exc:
            return Response(
                {"detail": str(exc.detail)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = get_user_data(user)

        return Response(
            {
                "access": str(access_token),
                "refresh": str(refresh_token),
                "user": user,
            },
            status=status.HTTP_200_OK,
        )
