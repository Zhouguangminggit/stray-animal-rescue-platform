from django.conf import settings
from django.db import models


class Activity(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "草稿"
        OPEN = "open", "报名中"
        CLOSED = "closed", "已关闭"
        COMPLETED = "completed", "已结束"
        CANCELLED = "cancelled", "已取消"

    title = models.CharField("活动名称", max_length=150)
    summary = models.CharField("摘要", max_length=300)
    content = models.TextField("活动说明")
    campus = models.ForeignKey(
        "campuses.Campus",
        on_delete=models.PROTECT,
        related_name="activities",
        verbose_name="校区",
    )
    location = models.CharField("活动地点", max_length=255)
    starts_at = models.DateTimeField("活动开始")
    ends_at = models.DateTimeField("活动结束")
    registration_starts_at = models.DateTimeField("报名开始")
    registration_ends_at = models.DateTimeField("报名结束")
    capacity = models.PositiveIntegerField("人数上限")
    status = models.CharField(
        "状态", max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    tags = models.ManyToManyField(
        "tags.Tag", related_name="activities", blank=True, verbose_name="标签"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "校园活动"
        verbose_name_plural = "校园活动"
        ordering = ("-starts_at",)

    def __str__(self) -> str:
        return self.title


class Participation(models.Model):
    class Status(models.TextChoices):
        REGISTERED = "registered", "已报名"
        CANCELLED = "cancelled", "已取消"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="activity_participations",
        verbose_name="参与者",
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.PROTECT,
        related_name="participations",
        verbose_name="活动",
    )
    status = models.CharField(
        "状态", max_length=20, choices=Status.choices, default=Status.REGISTERED
    )
    active_marker = models.BooleanField(default=True, null=True, editable=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "活动报名"
        verbose_name_plural = "活动报名"
        ordering = ("-registered_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "activity", "active_marker"),
                name="uniq_active_activity_user",
            )
        ]
        indexes = [
            models.Index(fields=("activity", "status"), name="activity_signup_idx")
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.activity}"
