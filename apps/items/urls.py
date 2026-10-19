from django.urls import path
from .views.item import CreateItemAPIView, AllItemsAPIView, AllStorefrontItemsAPIView
from .views.status import CreateStatusAPIView, AllStatusesAPIView

urlpatterns = [
    path("create/", CreateItemAPIView.as_view(), name="create-item"),
    path(
        "storefront/<str:storefront_id>/",
        AllStorefrontItemsAPIView.as_view(),
        name="all-storefront-items",
    ),
    path("all/", AllItemsAPIView.as_view(), name="all-items"),
    path("status/create/", CreateStatusAPIView.as_view(), name="create-status"),
    path("status/all/", AllStatusesAPIView.as_view(), name="all-statuses"),
]
