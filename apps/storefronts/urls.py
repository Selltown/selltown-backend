from django.urls import path
from .views import (
    ListAllStorefrontsAPIView,
    CreateStorefrontAPIView,
    RetrieveStorefrontAPIView,
)

urlpatterns = [
    path("all/", ListAllStorefrontsAPIView.as_view(), name="list-all-storefronts"),
    path("create/", CreateStorefrontAPIView.as_view(), name="create-storefront"),
    path(
        "<str:pk>/",
        RetrieveStorefrontAPIView.as_view(),
        name="retrieve-storefront",
    ),
]
