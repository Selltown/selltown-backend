from rest_framework import serializers
from ...crafts.models import Craft
from ..models.user import CustomUser
import logging

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
