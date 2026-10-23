from django.db import models
import uuid
from ...users.models.artisan import ArtisanProfile
from django.db.models.functions import Lower


class Storefront(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(
        ArtisanProfile, on_delete=models.CASCADE, related_name="storefronts"
    )
    name = models.CharField(max_length=225)
    image = models.ImageField(upload_to="storefronts/", null=True, blank=True)

    class Meta:
        db_table = "storefronts"
        verbose_name = "storefront"
        verbose_name_plural = "storefronts"

        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="unique_storefront_name_case_insensitive"
            )
        ]

    def __str__(self):
        return self.name
