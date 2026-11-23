from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        exclude = ["id"]
        extra_kwargs = {
            "place_id": {
                "validators": [],
                "required": True,
                "allow_blank": False,
            }
        }

    def validate(self, attrs):
        required_fields = [
            "place_id",
            "name",
            "city",
            "full_address",
            "region",
            "longitude",
            "latitude",
        ]

        errors = {}

        for field in required_fields:
            if field not in attrs or not attrs[field].strip():
                errors[field] = "This field is required."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
