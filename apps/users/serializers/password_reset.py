from rest_framework import serializers


class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class PasswordResetVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(max_length=6)
