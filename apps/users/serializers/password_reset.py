from rest_framework import serializers


class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
