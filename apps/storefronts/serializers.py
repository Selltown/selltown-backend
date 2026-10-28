from rest_framework import serializers
from .models.storefront import Storefront
from ..locations.models import Location
from django.db import transaction
from .utils import generate_unique_slug
from .models.storefront_slug import StorefrontSlug


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        exclude = ["id"]


class ListAllStorefrontsSerializer(serializers.ModelSerializer):
    storefront_id = serializers.UUIDField(source="id", read_only=True)
    storefront_name = serializers.ReadOnlyField(source="name")
    storefront_image = serializers.ImageField(source="image")
    craft_name = serializers.ReadOnlyField(source="artisan.craft.craft_name")
    location = LocationSerializer(source="artisan.location")

    class Meta:
        model = Storefront
        fields = [
            "storefront_id",
            "storefront_name",
            "storefront_image",
            "craft_name",
            "location",
        ]


class CreateStorefrontSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storefront
        fields = ["id", "name", "image"]

    @transaction.atomic
    def create(self, validated_data):
        storefront = Storefront.objects.create(**validated_data)

        StorefrontSlug.objects.create(
            storefront=storefront, slug=generate_unique_slug(storefront.name)
        )

        return storefront


class RetrieveStorefrontSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storefront
        fields = ["id", "name", "image"]
