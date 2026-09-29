import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import logging

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):

    def create_user(self, phone_number, name, password):
        if not phone_number:
            logger.error("Phone number was not provided during user creation.")
            raise ValueError("User must have a phone number.")
        if not name:
            logger.error("Name was not provided during user creation.")
            raise ValueError("User must have a name.")
        if not password:
            logger.error("Password was not provided during user creation.")
            raise ValueError("User must have a password.")

        user = self.model(phone_number=phone_number, name=name)
        user.set_password(password)
        user.save(using=self._db)
        logger.info("User saved successfully.")

        return user

    def create_superuser(self, phone_number, name, password):
        user = self.create_user(phone_number, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        logger.info("User saved successfully.")

        return user


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = PhoneNumberField(unique=True, region="GH")
    name = models.CharField(max_length=125)
    is_phone_verified = models.BooleanField(default=False)

    username = None

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"({self.name}) ({self.phone_number})"
