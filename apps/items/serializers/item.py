from rest_framework import serializers
from ..models.item import Item


class CreateItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"


class ReadItemSerializer(serializers.ModelSerializer):
    item_id = serializers.UUIDField(source="id", read_only=True)
    storefront_id = serializers.UUIDField(
        source="storefront.id",
        read_only=True,
    )
    storefront_name = serializers.ReadOnlyField(source="storefront.name")
    status_id = serializers.ReadOnlyField(
        source="status.id",
        read_only=True,
    )
    status_name = serializers.ReadOnlyField(source="status.name")

    class Meta:
        model = Item
        fields = [
            "item_id",
            "storefront_id",
            "storefront_name",
            "status_id",
            "status_name",
            "price",
            "image",
            "description",
        ]
