from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other):
        other.setdefault("is_staff", True)
        other.setdefault("is_superuser", True)
        other.setdefault("is_active", True)

        if other.get("is_staff") is not True:
            raise ValueError("Superuser must be staff")

        if other.get("is_superuser") is not True:
            raise ValueError("Superuser must be is_superuser=True")

        return self.create_user(email, password)

    def create_user(self, email, password, **other):
        if not email:
            raise ValueError("You must provide an email")

        email = self.normalize_email(email)
        user = self.model(
            email=email, **other
        )
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.user_name
