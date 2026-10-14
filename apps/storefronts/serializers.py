from rest_framework import serializers
from .models import Storefront


class ListAllStorefrontsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storefront
        fields = "__all__"


class CreateStorefrontSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storefront
        fields = ["name", "image"]
