from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    kor_name = models.CharField(
        "한글 이름", max_length=20, null=False, blank=True, default=""
    )
    first_name = None
    last_name = None
    email = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "user"
