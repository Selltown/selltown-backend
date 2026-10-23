from django.db import models
import uuid
from ...storefronts.models.storefront import Storefront
from .status import Status


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="items/", blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="items")
    storefront = models.ForeignKey(
        Storefront, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        db_table = "items"
        verbose_name = "item"
        verbose_name_plural = "items"

    def __str__(self):
        return self.name
