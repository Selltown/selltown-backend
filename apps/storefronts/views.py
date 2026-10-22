from rest_framework import generics, serializers
from .serializers import ListAllStorefrontsSerializer, CreateStorefrontSerializer
from .models import Storefront
from rest_framework.permissions import IsAuthenticated
from .permissions import IsArtisan
from .throttles import CreateStorefrontThrottle
from ..common.pagination import StandardResultSetPagination


class ListAllStorefrontsAPIView(generics.ListAPIView):
    serializer_class = ListAllStorefrontsSerializer
    queryset = Storefront.objects.select_related("artisan", "artisan__user")
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultSetPagination


class CreateStorefrontAPIView(generics.CreateAPIView):
    serializer_class = CreateStorefrontSerializer
    queryset = Storefront.objects.all()
    permission_classes = [IsAuthenticated, IsArtisan]
    throttle_classes = [CreateStorefrontThrottle]

    def perform_create(self, serializer):
        artisan = self.request.user.artisan_profile

        if artisan.storefronts.exists():
            serializers.ValidationError({"detail": "You already have a storefront."})

        serializer.save(artisan=artisan)
