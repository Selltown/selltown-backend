from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class VerifyOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()
