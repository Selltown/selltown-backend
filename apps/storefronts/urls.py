from django.urls import path
from .views import ListAllStorefrontsAPIView, CreateStorefrontAPIView

urlpatterns = [
    path("all/", ListAllStorefrontsAPIView.as_view(), name="list-all-storefronts"),
    path("create/", CreateStorefrontAPIView.as_view(), name="create-storefront"),
]
