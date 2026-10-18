from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "statuses"
        verbose_name = "status"
        verbose_name_plural = "statuses"

    def __str__(self):
        return self.name
