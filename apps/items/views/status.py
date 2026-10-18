from ..serializers.status import StatusSerializer
from ..models.status import Status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from ..throttles import CreateItemThrottle


class CreateStatusAPIView(generics.CreateAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    throttle_classes = [CreateItemThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]


class AllStatusesAPIView(generics.ListAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None
