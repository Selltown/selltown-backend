from rest_framework import serializers
from .models import Storefront
from ..locations.models import Location


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


class StorefrontSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storefront
        fields = ["id", "name", "image"]
