import uuid
from pathlib import Path
from typing import ClassVar

from django.contrib.auth.models import (
    AbstractUser,
)
from django.contrib.auth.models import (
    UserManager as DjangoUserManager,
)
from django.db import models


class UserManager(DjangoUserManager["User"]):
    """Typed extension point for account creation rules."""


def avatar_upload_to(instance: "User", filename: str) -> str:
    extension = Path(filename).suffix.lower() or ".jpg"
    return f"avatars/{instance.pk}/{uuid.uuid4().hex}{extension}"


class User(AbstractUser):
    nickname = models.CharField("昵称", max_length=50, blank=True)
    avatar = models.ImageField("头像", upload_to=avatar_upload_to, blank=True)
    email = models.EmailField("邮箱", unique=True)
    phone = models.CharField(
        "手机号", max_length=20, unique=True, null=True, blank=True
    )
    campus = models.ForeignKey(
        "campuses.Campus",
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
        verbose_name="所属校区",
    )
    student_number = models.CharField("学号/工号", max_length=50, blank=True)
    identity_note = models.CharField("身份说明", max_length=100, blank=True)

    objects: ClassVar[UserManager] = UserManager()

    @property
    def display_name(self) -> str:
        if self.nickname.strip():
            return self.nickname.strip()
        if self.phone and self.username.startswith("mobile_"):
            return f"{self.phone[:3]}****{self.phone[-4:]}"
        return self.username

    def __str__(self) -> str:
        return self.display_name
