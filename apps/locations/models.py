from django.db import models
import uuid


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    full_address = models.CharField(max_length=500)
    region = models.CharField(max_length=255)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)

    def __str__(self):
        return f"({self.city}) ({self.full_address})"
