from django.db import models
import uuid


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place_id = models.CharField()
    name = models.CharField()
    city = models.CharField()
    full_address = models.CharField()
    region = models.CharField()
    longitude = models.CharField()
    latitude = models.CharField()

    def __str__(self):
        return f"({self.city}) ({self.full_address})"
