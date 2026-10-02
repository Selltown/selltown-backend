from django.urls import path
from .views.user import CreateUserView, LoginView, VerifyOTPView, ResendOTPView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create-user"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend-otp"),
]
