from ..serializers.status import StatusSerializer
from ..models.status import Status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class AllStatusesAPIView(generics.ListAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None
