import uuid
from django.db import models
from .user import CustomUser


class CustomerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="customer_profile"
    )

    class Meta:
        db_table = "customer_profiles"
        verbose_name = "customer profile"
        verbose_name_plural = "customer profiles"

    def __str__(self):
        return f"{self.user.name} - {self.user.phone_number}"
