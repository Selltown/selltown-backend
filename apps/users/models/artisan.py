import uuid
from django.db import models
from .user import CustomUser
from ...locations.models import Location
from ...crafts.models import Craft


class ArtisanProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="artisan_profile"
    )
    craft = models.ForeignKey(Craft, on_delete=models.PROTECT, related_name="artisans")
    location = models.OneToOneField(
        Location, on_delete=models.PROTECT, related_name="artisans"
    )

    class Meta:
        db_table = "artisan_profiles"
        verbose_name = "artisan profile"
        verbose_name_plural = "artisan profiles"

    def __str__(self):
        return (
            f"({self.user.name}) ({self.user.phone_number}) ({self.craft.craft_name})"
        )
