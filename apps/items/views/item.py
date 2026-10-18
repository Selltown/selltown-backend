from ..serializers.item import CreateItemSerializer, ReadItemSerializer
from ..models.item import Item
from ..throttles import CreateItemThrottle
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsArtisan
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class CreateItemAPIView(generics.CreateAPIView):
    serializer_class = CreateItemSerializer
    queryset = Item.objects.select_related("storefront", "status")
    throttle_classes = [CreateItemThrottle]
    permission_classes = [IsAuthenticated, IsArtisan]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        read_item = ReadItemSerializer(
            serializer.instance, context=self.get_serializer_context()
        ).data

        return Response(read_item, status=status.HTTP_201_CREATED, headers=headers)
