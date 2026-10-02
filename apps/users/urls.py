from django.urls import path
from .views.user import CreateUserView, LoginView, VerifyOTPView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create-user"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
]
