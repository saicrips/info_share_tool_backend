from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.contrib.auth.models import User

import hashlib
from datetime import timedelta
from django.utils import timezone


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance is not None:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.full_clean()

        Token.objects.create(user=user)

        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields["is_active"] = True
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="username", unique=True, max_length=150, primary_key=True
    )
    email = models.EmailField(verbose_name="Email Address", unique=True)
    first_name = models.CharField(
        verbose_name="first_name", null=True, blank=True, max_length=100
    )
    last_name = models.CharField(
        verbose_name="last_name", null=True, blank=True, max_length=100
    )
    age = models.IntegerField(verbose_name="age", null=True, blank=True)
    description = models.CharField(
        verbose_name="description", null=True, blank=True, max_length=200
    )
    is_superuser = models.BooleanField(verbose_name="is_superuer", default=False)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
    )
    is_active = models.BooleanField(
        "active",
        default=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
