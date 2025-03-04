from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username and not email:
            raise ValueError("Either username or email must be provided")
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)

    profile_picture = models.URLField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    t_shirt_size = models.CharField(max_length=10, null=True, blank=True)

    country = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True) # School, College, University or Company

    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
