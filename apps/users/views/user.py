from ..models.user import CustomUser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from ..serializers.user import CreateUserSerializer
from ..throttles import RegistrationThrottle
from ..services.otp.arkesel import send_otp, ArkeselError, verify_otp
from rest_framework import generics
from ..serializers.authentication import (
    LoginSerializer,
    VerifyOtpSerializer,
    ResendOtpSerializer,
    LogoutSerializer,
)
from ..throttles import LoginThrottle, OTPThrottle, LogoutThrottle
from rest_framework.exceptions import AuthenticationFailed
from ..services.user import get_user_data
from ..services.authentication import (
    authenticate_user,
    generate_tokens_for_user,
    blacklist_refresh_token,
)
from ..services.user import create_user
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError


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


class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer
    throttle_classes = [OTPThrottle]

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

        access_token, refresh_token, user = generate_tokens_for_user(
            serializer.validated_data["phone_number"]
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


class ResendOTPView(generics.GenericAPIView):
    serializer_class = ResendOtpSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            data = send_otp(serializer.validated_data["phone_number"])
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


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    throttle_classes = [LogoutThrottle]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh_token"]

        try:
            blacklist_refresh_token(refresh_token)

            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)

        except TokenError:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListAllUsersAPIView(generics.ListAPIView): ...
