from django.db import models
from .storefront import Storefront
from django.db.models import Q


class StorefrontSlug(models.Model):
    storefront = models.ForeignKey(
        Storefront, on_delete=models.CASCADE, related_name="slug_history"
    )
    slug = models.SlugField(max_length=255, unique=True)
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "storefront_slugs"
        verbose_name = "storefront_slugs"
        verbose_name_plural = "storefront_slugs"
        constraints = [
            models.UniqueConstraint(
                fields=["storefront"],
                condition=Q(is_current=True),
                name="one_current_slug_per_storefront",
            )
        ]

    def __str__(self):
        return self.slug
