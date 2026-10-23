from django.urls import path
from .views import (
    ListAllStorefrontsAPIView,
    CreateStorefrontAPIView,
    RetrieveStorefrontAPIView,
    CheckStorefrontNameAPIView,
)

urlpatterns = [
    path("all/", ListAllStorefrontsAPIView.as_view(), name="list-all-storefronts"),
    path("create/", CreateStorefrontAPIView.as_view(), name="create-storefront"),
    path(
        "check-name/",
        CheckStorefrontNameAPIView.as_view(),
        name="check-storefront-name",
    ),
    path(
        "<str:pk>/",
        RetrieveStorefrontAPIView.as_view(),
        name="retrieve-storefront",
    ),
]
