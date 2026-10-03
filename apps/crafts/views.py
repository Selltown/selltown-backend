from rest_framework import generics
from .models import Craft
from .serializers import CraftSerializer


class ListCraftsAPIView(generics.ListAPIView):
    queryset = Craft.objects.all()
    serializer_class = CraftSerializer
