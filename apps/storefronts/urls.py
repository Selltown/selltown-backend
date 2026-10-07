from django.urls import path
from .views import ListAllStorefrontsAPIView

urlpatterns = [
    path("all/", ListAllStorefrontsAPIView.as_view(), name="list-all-storefronts"),
]
