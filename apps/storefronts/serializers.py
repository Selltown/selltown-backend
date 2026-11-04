from rest_framework import serializers
from .models.storefront import Storefront
from ..locations.models import Location
from django.db import transaction
from .utils import generate_unique_slug
from .models.storefront_slug import StorefrontSlug

# todo: Add logs in all parts of the application without it


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
    current_slug = serializers.SerializerMethodField()

    class Meta:
        model = Storefront
        fields = [
            "storefront_id",
            "storefront_name",
            "storefront_image",
            "craft_name",
            "location",
            "current_slug",
        ]

    def get_current_slug(self, obj):
        current_slugs = obj.current_slug_records

        if current_slugs:
            return current_slugs[0].slug

        return None


class CreateStorefrontSerializer(serializers.ModelSerializer):
    current_slug = serializers.SerializerMethodField()

    class Meta:
        model = Storefront
        fields = ["id", "name", "image", "current_slug"]

    def get_current_slug(self, obj):
        current_slug = obj.slug_history.filter(is_current=True).first()

        return current_slug.slug if current_slug else None

    @transaction.atomic
    def create(self, validated_data):
        storefront = Storefront.objects.create(**validated_data)

        StorefrontSlug.objects.create(
            storefront=storefront, slug=generate_unique_slug(storefront.name)
        )

        return storefront


class UpdateStorefrontSerializer(serializers.ModelSerializer):
    current_slug = serializers.SerializerMethodField()

    class Meta:
        model = Storefront
        fields = ["id", "name", "image", "current_slug"]

    def get_current_slug(self, obj):
        current_slug = obj.slug_history.filter(is_current=True).first()

        return current_slug.slug if current_slug else None

    def validate_name(self, value):
        value = value.strip()

        duplicates = Storefront.objects.filter(name__iexact=value)

        if self.instance:
            duplicates = duplicates.exclude(pk=self.instance.pk)

        if duplicates.exists():
            raise serializers.ValidationError(
                "A storefront with this name already exists."
            )

        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        new_name = validated_data.get("name", instance.name)
        name_changed = new_name != instance.name

        if name_changed:
            StorefrontSlug.objects.filter(
                storefront=instance,
                is_current=True,
            ).update(is_current=False)

        instance = super().update(instance, validated_data)

        if name_changed:
            StorefrontSlug.objects.create(
                storefront=instance,
                slug=generate_unique_slug(new_name),
                is_current=True,
            )

        return instance


class RetrieveStorefrontSerializer(serializers.ModelSerializer):
    location = LocationSerializer(source="artisan.location", read_only=True)

    class Meta:
        model = Storefront
        fields = ["id", "name", "image", "location"]
