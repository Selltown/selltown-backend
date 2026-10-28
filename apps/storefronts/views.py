from rest_framework import generics, serializers
from .serializers import (
    ListAllStorefrontsSerializer,
    CreateStorefrontSerializer,
    RetrieveStorefrontSerializer,
)
from .models import Storefront
from rest_framework.permissions import IsAuthenticated
from .permissions import IsArtisan
from .throttles import CreateStorefrontThrottle
from ..common.pagination import StandardResultSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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


class RetrieveStorefrontAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveStorefrontSerializer
    queryset = Storefront.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    throttle_classes = []


class CheckStorefrontNameAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.query_params.get("name", "").strip()

        if not name:
            return Response(
                {"available": False, "detail": "Storefront name is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(name) > 225:
            return Response(
                {
                    "available": False,
                    "detail": "Storefront name cannot exceed 255 characters.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        name_exists = Storefront.objects.filter(name__iexact=name).exists()
        return Response(
            {
                "available": not name_exists,
                "detail": (
                    "Name is already taken." if name_exists else "Name is available."
                ),
            },
            status=status.HTTP_200_OK,
        )
