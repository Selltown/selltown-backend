from django.urls import path
from .views.user import (
    CreateUserView,
    LoginView,
    VerifyOTPView,
    ResendOTPView,
    LogoutView,
)
from .views.password_reset import PasswordResetRequestAPIView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create-user"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend-otp"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password-reset/request/",
        PasswordResetRequestAPIView.as_view(),
        name="password-reset-request",
    ),
]
