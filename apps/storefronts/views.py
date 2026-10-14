from rest_framework import generics
from .serializers import ListAllStorefrontsSerializer, CreateStorefrontSerializer
from .models import Storefront
from rest_framework.permissions import IsAuthenticated
from .permissions import IsArtisan
from .throttles import CreateStorefrontThrottle


class ListAllStorefrontsAPIView(generics.ListAPIView):
    serializer_class = ListAllStorefrontsSerializer
    queryset = Storefront.objects.all()
    permission_classes = [IsAuthenticated]


class CreateStorefrontAPIView(generics.CreateAPIView):
    serializer_class = CreateStorefrontSerializer
    queryset = Storefront.objects.all()
    permission_classes = [IsAuthenticated, IsArtisan]
    throttle_classes = [CreateStorefrontThrottle]

    def perform_create(self, serializer):
        serializer.save(artisan=self.request.user.artisan_profile)
