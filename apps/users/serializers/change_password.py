from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import logging

logger = logging.getLogger(__name__)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value, self.context["request"].user)
        logger.info("New password is valid.")

        return value
