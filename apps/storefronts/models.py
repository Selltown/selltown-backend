from django.db import models
import uuid


class Storefront(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225, editable=False)
    image = models.ImageField(upload_to="storefronts/", null=True, blank=True)

    class Meta:
        db_table = "storefronts"
        verbose_name = "storefront"
        verbose_name_plural = "storefronts"

    def __str__(self):
        return self.name
