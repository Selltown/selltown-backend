from rest_framework import generics, serializers
from .serializers import (
    ListAllStorefrontsSerializer,
    CreateStorefrontSerializer,
    RetrieveStorefrontSerializer,
    UpdateStorefrontSerializer,
)
from .models import Storefront
from rest_framework.permissions import IsAuthenticated
from .permissions import IsArtisan
from .throttles import CreateStorefrontThrottle
from ..common.pagination import StandardResultSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models.storefront_slug import StorefrontSlug
from django.db.models import Prefetch


class ListAllStorefrontsAPIView(generics.ListAPIView):
    serializer_class = ListAllStorefrontsSerializer
    queryset = Storefront.objects.select_related(
        "artisan__craft", "artisan__location"
    ).prefetch_related(
        Prefetch(
            "slug_history",
            queryset=StorefrontSlug.objects.filter(is_current=True),
            to_attr="current_slug_records",
        )
    )
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
            raise serializers.ValidationError(
                {"detail": "You already have a storefront."}
            )

        serializer.save(artisan=artisan)


class UpdateStorefrontAPIView(generics.UpdateAPIView):
    serializer_class = UpdateStorefrontSerializer
    permission_classes = [IsAuthenticated, IsArtisan]
    throttle_classes = [CreateStorefrontThrottle]

    def get_queryset(self):
        return Storefront.objects.filter(artisan__user=self.request.user)


class RetrieveStorefrontBySlugAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveStorefrontSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = []
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        return StorefrontSlug.objects.select_related("storefront").all()

    def retrieve(self, request, *args, **kwargs):
        slug_record = self.get_object()
        storefront = slug_record.storefront

        current_slug = StorefrontSlug.objects.get(
            storefront=storefront, is_current=True
        )

        serializer = self.get_serializer(storefront)

        return Response(
            {
                "storefront": serializer.data,
                "current_slug": current_slug.slug,
                "is_current_slug": slug_record.is_current,
            },
            status=status.HTTP_200_OK,
        )


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
