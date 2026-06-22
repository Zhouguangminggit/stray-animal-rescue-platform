from django.conf import settings
from django.db import models
from django.db.models import Sum


class DonationProject(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "草稿"
        OPEN = "open", "进行中"
        CLOSED = "closed", "已关闭"
        COMPLETED = "completed", "已完成"

    title = models.CharField("项目名称", max_length=150)
    summary = models.CharField("摘要", max_length=300)
    description = models.TextField("项目说明")
    status = models.CharField(
        "状态", max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    starts_at = models.DateTimeField("开始时间")
    ends_at = models.DateTimeField("结束时间")
    tags = models.ManyToManyField(
        "tags.Tag", related_name="donation_projects", blank=True, verbose_name="标签"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "捐赠项目"
        verbose_name_plural = "捐赠项目"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title


class DonationItem(models.Model):
    project = models.ForeignKey(
        DonationProject,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="项目",
    )
    name = models.CharField("物资名称", max_length=100)
    unit = models.CharField("单位", max_length=20)
    required_quantity = models.PositiveIntegerField("需求数量")
    sort_order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        verbose_name = "需求物资"
        verbose_name_plural = "需求物资"
        ordering = ("sort_order", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("project", "name"), name="uniq_donation_project_item"
            )
        ]

    def __str__(self) -> str:
        return f"{self.project} - {self.name}"

    @property
    def pledged_quantity(self) -> int:
        return (
            self.pledges.filter(
                status__in=(Pledge.Status.PLEDGED, Pledge.Status.CONFIRMED)
            ).aggregate(total=Sum("quantity"))["total"]
            or 0
        )

    @property
    def remaining_quantity(self) -> int:
        return max(self.required_quantity - self.pledged_quantity, 0)


class Pledge(models.Model):
    class Status(models.TextChoices):
        PLEDGED = "pledged", "待交付"
        CONFIRMED = "confirmed", "已确认"
        CANCELLED = "cancelled", "已取消"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pledges",
        verbose_name="认捐人",
    )
    item = models.ForeignKey(
        DonationItem,
        on_delete=models.PROTECT,
        related_name="pledges",
        verbose_name="物资",
    )
    quantity = models.PositiveIntegerField("认捐数量")
    note = models.CharField("备注", max_length=255, blank=True)
    status = models.CharField(
        "状态", max_length=20, choices=Status.choices, default=Status.PLEDGED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "物资认捐"
        verbose_name_plural = "物资认捐"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("item", "status"), name="pledge_item_status_idx")
        ]

    def __str__(self) -> str:
        return f"{self.user} 认捐 {self.item}"
