from rest_framework import serializers
from .models import Craft


class CraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Craft
        fields = "__all__"
