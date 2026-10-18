from django.urls import path
from .views.item import CreateItemAPIView
from .views.status import CreateStatusAPIView, AllStatusesAPIView

urlpatterns = [
    path("create/", CreateItemAPIView.as_view(), name="create-item"),
    path("status/create/", CreateStatusAPIView.as_view(), name="create-status"),
    path("status/all/", AllStatusesAPIView.as_view(), name="all-statuses"),
]
