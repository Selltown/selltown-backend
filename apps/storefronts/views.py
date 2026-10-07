from rest_framework import generics
from .serializers import ListAllStorefrontsSerializer
from .models import Storefront
from rest_framework.permissions import IsAuthenticated


class ListAllStorefrontsAPIView(generics.ListAPIView):
    serializer_class = ListAllStorefrontsSerializer
    queryset = Storefront.objects.all()
    permission_classes = [IsAuthenticated]
