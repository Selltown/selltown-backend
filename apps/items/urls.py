from django.urls import path
from .views.item import CreateItemAPIView, AllStorefrontItemsAPIView
from .views.status import AllStatusesAPIView

urlpatterns = [
    path("create/", CreateItemAPIView.as_view(), name="create-item"),
    path(
        "storefront/<slug:slug>/",
        AllStorefrontItemsAPIView.as_view(),
        name="all-storefront-items",
    ),
    path("status/all/", AllStatusesAPIView.as_view(), name="all-statuses"),
]
