from django.conf import settings
from django.db import models


class Notification(models.Model):
    class BusinessType(models.TextChoices):
        SYSTEM = "system", "系统"
        RESCUE = "rescue", "救助"
        ADOPTION = "adoption", "领养"
        VOLUNTEER = "volunteer", "志愿者"
        REPORT = "report", "举报"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="接收人",
    )
    business_type = models.CharField(
        "业务类型",
        max_length=20,
        choices=BusinessType.choices,
        default=BusinessType.SYSTEM,
    )
    title = models.CharField("标题", max_length=100)
    content = models.TextField("内容")
    related_app = models.CharField("关联应用", max_length=50, blank=True)
    related_object_id = models.PositiveBigIntegerField(
        "关联对象ID", null=True, blank=True
    )
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    read_at = models.DateTimeField("已读时间", null=True, blank=True)

    class Meta:
        verbose_name = "站内通知"
        verbose_name_plural = "站内通知"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("recipient", "read_at", "-created_at"),
                name="notice_user_read_idx",
            )
        ]

    def __str__(self) -> str:
        return self.title
