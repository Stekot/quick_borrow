import uuid as uuid_module
from typing import Any, Optional

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str | None, **extra_fields: Any) -> "User":
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user: "User" = self.model(email=email, username=email, **extra_fields)

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, editable=False, default=uuid_module.uuid4)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=150, null=True, blank=True, default=None)  # noqa: DJ01

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list = []

    def __str__(self) -> str:
        return f"{self.full_name} - {self.email}"

    def get_full_name(self) -> str:
        return self.full_name
