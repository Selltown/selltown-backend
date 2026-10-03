from django.urls import path
from .views import ListCraftsAPIView

urlpatterns = [
    path("all/", ListCraftsAPIView.as_view(), name="all-crafts"),
]
