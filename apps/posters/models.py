import uuid
from pathlib import Path
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.core.validators import validate_image_size


def poster_upload_to(instance: object, filename: str) -> str:
    extension = Path(filename).suffix.lower() or ".jpg"
    return f"posters/{uuid.uuid4().hex}{extension}"


class Poster(models.Model):
    class Page(models.TextChoices):
        HOME = "home", "首页"
        RESCUE = "rescue", "救助信息"
        ADOPTION = "adoption", "领养中心"
        VOLUNTEER = "volunteer", "志愿者社区"
        DONATION = "donation", "爱心捐赠"
        ACTIVITY = "activity", "校园活动"

    class Slot(models.TextChoices):
        BANNER = "banner", "Banner 轮播"
        QUICK_ENTRY = "quick_entry", "金刚区入口"
        MODULE_CARD = "module_card", "模块卡片"
        PUBLIC_WELFARE = "public_welfare", "公益海报"

    title = models.CharField("标题", max_length=150)
    subtitle = models.CharField("副标题", max_length=300, blank=True)
    image = models.ImageField(
        "海报图片", upload_to=poster_upload_to, validators=(validate_image_size,)
    )
    link = models.CharField("跳转链接", max_length=500, blank=True)
    page = models.CharField(
        "展示页面", max_length=20, choices=Page.choices, default=Page.HOME
    )
    slot = models.CharField("展示位", max_length=30, choices=Slot.choices)
    sort_order = models.PositiveIntegerField("排序", default=0)
    starts_at = models.DateTimeField("生效时间", null=True, blank=True)
    ends_at = models.DateTimeField("失效时间", null=True, blank=True)
    is_active = models.BooleanField("启用", default=True)
    tags = models.ManyToManyField(
        "tags.Tag", related_name="posters", blank=True, verbose_name="标签"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "海报"
        verbose_name_plural = "海报"
        ordering = ("sort_order", "-created_at")
        indexes = [
            models.Index(
                fields=("page", "slot", "is_active"), name="poster_position_idx"
            )
        ]

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        if self.starts_at and self.ends_at and self.starts_at >= self.ends_at:
            raise ValidationError({"ends_at": "失效时间必须晚于生效时间。"})
        if self.link:
            parsed = urlparse(self.link)
            if not self.link.startswith("/") and parsed.scheme not in {"http", "https"}:
                raise ValidationError({"link": "仅支持站内路径或 HTTP/HTTPS 链接。"})

    @classmethod
    def active_for(cls, *, page: str, slot: str):
        now = timezone.now()
        return (
            cls.objects.filter(page=page, slot=slot, is_active=True)
            .filter(models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now))
            .filter(models.Q(ends_at__isnull=True) | models.Q(ends_at__gt=now))
        )
