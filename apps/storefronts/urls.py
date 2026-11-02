from django.urls import path
from .views import (
    ListAllStorefrontsAPIView,
    CreateStorefrontAPIView,
    RetrieveStorefrontBySlugAPIView,
    CheckStorefrontNameAPIView,
    UpdateStorefrontAPIView,
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
        "by-slug/<slug:slug>/",
        RetrieveStorefrontBySlugAPIView.as_view(),
        name="retrieve-storefront-by-slug",
    ),
    path(
        "<uuid:pk>/update/",
        UpdateStorefrontAPIView.as_view(),
        name="update-storefront",
    ),
]
