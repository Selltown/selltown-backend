from rest_framework import serializers
from .models import Storefront


class ListAllStorefrontsSerializer(serializers.ModelSerializer):
    storefront_id = serializers.UUIDField(source="id", read_only=True)
    artisan_id = serializers.ReadOnlyField(source="artisan.id")
    artisan_name = serializers.ReadOnlyField(source="artisan.user.name")

    class Meta:
        model = Storefront
        fields = [
            "storefront_id",
            "name",
            "image",
            "artisan_id",
            "artisan_name",
        ]


class CreateStorefrontSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storefront
        fields = ["id", "name", "image"]
