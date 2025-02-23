from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    profile_picture = models.URLField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

