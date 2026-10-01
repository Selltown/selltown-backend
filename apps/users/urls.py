from django.urls import path
from .views.user import CreateUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create-user"),
]
