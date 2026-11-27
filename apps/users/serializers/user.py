from rest_framework import serializers
from ...crafts.models import Craft
from ..models.user import CustomUser
import logging
from ...locations.models import Location
from ..models.artisan import ArtisanProfile
from ...locations.serializers import LocationSerializer
from django.db import transaction

logger = logging.getLogger(__name__)


class CreateUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=["customer", "artisan"], write_only=True)
    craft = serializers.PrimaryKeyRelatedField(
        queryset=Craft.objects.all(), required=False, write_only=True
    )
    location = serializers.JSONField(required=False, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "phone_number",
            "name",
            "password",
            "role",
            "craft",
            "location",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        artisan_fields = ["craft", "location"]
        artisan_location_fields = [
            "name",
            "place_id",
            "city",
            "longitude",
            "latitude",
            "region",
            "full_address",
        ]

        if attrs["role"] == "artisan":
            for field in artisan_fields:
                # Ensure location & craft fields are required for artisans
                if not attrs.get(field):
                    logger.error(
                        f"{field} is required for artisans or cannot be blank."
                    )
                    raise serializers.ValidationError(
                        {field: "This field may not be blank."}
                    )

            # Ensure all required fields in location are not null
            for location_field in artisan_location_fields:

                location = attrs.get("location")

                if not location.get(location_field):
                    logger.error(f"{location_field} is required.")
                    raise serializers.ValidationError(
                        {location_field: f"This field is required."}
                    )

        return attrs


class UpdateUserSerializer(serializers.ModelSerializer):
    craft = serializers.PrimaryKeyRelatedField(
        queryset=Craft.objects.all(), required=False
    )
    craft_description = serializers.CharField(required=False)
    location = LocationSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ["phone_number", "name", "craft", "craft_description", "location"]

    @transaction.atomic
    def update(self, instance, validated_data):
        phone_number_changed = (
            "phone_number" in validated_data
            and validated_data["phone_number"] != instance.phone_number
        )

        if phone_number_changed:
            validated_data["is_phone_verified"] = False

        artisan_data = {
            field: validated_data.pop(field)
            for field in ["craft", "craft_description", "location"]
            if field in validated_data
        }

        instance = super().update(instance, validated_data)

        if artisan_data:
            if not hasattr(instance, "artisan_profile"):
                raise serializers.ValidationError(
                    "Only artisans can update craft and location."
                )

            location_data = artisan_data.pop("location", None)
            artisan_profile = instance.artisan_profile

            for field, value in artisan_data.items():
                setattr(artisan_profile, field, value)

            if artisan_data:
                artisan_profile.save()

            if location_data is not None:
                location, created = Location.objects.get_or_create(
                    place_id=location_data["place_id"], defaults=location_data
                )

                artisan_profile.location = location
                artisan_profile.save(update_fields=["location"])

        return instance


class ReadArtisanSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source="artisan_profile.user.id")
    craft = serializers.ReadOnlyField(source="artisan_profile.craft.craft_name")
    craft_description = serializers.ReadOnlyField(
        source="artisan_profile.craft_description"
    )
    location = LocationSerializer(source="artisan_profile.location", read_only=True)
    storefront_id = serializers.SerializerMethodField()
    storefront_name = serializers.SerializerMethodField()
    current_slug = serializers.SerializerMethodField()

    def get_storefront_id(self, obj):
        storefront = obj.artisan_profile.storefronts.first()
        return storefront.id if storefront else None

    def get_storefront_name(self, obj):
        storefront = obj.artisan_profile.storefronts.first()
        return storefront.name if storefront else None

    def get_current_slug(self, obj):
        storefront = obj.artisan_profile.storefronts.first()

        if not storefront:
            return None

        current_slug = storefront.slug_history.filter(is_current=True).first()

        return current_slug.slug if current_slug else None

    class Meta:
        model = CustomUser
        fields = [
            "user_id",
            "phone_number",
            "is_phone_verified",
            "name",
            "craft",
            "craft_description",
            "location",
            "storefront_id",
            "storefront_name",
            "current_slug",
        ]


class ReadCustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source="customer_profile.user.id")

    class Meta:
        model = CustomUser
        fields = ["user_id", "phone_number", "name", "is_phone_verified"]
