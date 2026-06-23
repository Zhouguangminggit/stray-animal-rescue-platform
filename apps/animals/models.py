import uuid
from pathlib import Path

from django.conf import settings
from django.db import models

from apps.core.validators import validate_image_size


def animal_image_upload_to(instance: object, filename: str) -> str:
    extension = Path(filename).suffix.lower() or ".jpg"
    return f"animals/{uuid.uuid4().hex}{extension}"


def rescue_image_upload_to(instance: object, filename: str) -> str:
    extension = Path(filename).suffix.lower() or ".jpg"
    return f"rescue-requests/{uuid.uuid4().hex}{extension}"


class ReviewStatus(models.TextChoices):
    PENDING = "pending", "待审核"
    APPROVED = "approved", "已通过"
    REJECTED = "rejected", "已驳回"
    CANCELLED = "cancelled", "已取消"


class HealthStatus(models.TextChoices):
    HEALTHY = "healthy", "健康"
    INJURED = "injured", "受伤"
    SICK = "sick", "患病"
    RECOVERING = "recovering", "康复中"
    UNKNOWN = "unknown", "未知"


class Gender(models.TextChoices):
    MALE = "male", "公"
    FEMALE = "female", "母"
    UNKNOWN = "unknown", "未知"


class AnimalCategory(models.Model):
    name = models.CharField("分类名称", max_length=50, unique=True)
    sort_order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "动物分类"
        verbose_name_plural = "动物分类"
        ordering = ("sort_order", "id")

    def __str__(self) -> str:
        return self.name


class Animal(models.Model):
    class RescueStatus(models.TextChoices):
        WAITING = "waiting", "待救助"
        RESCUED = "rescued", "已救助"

    class AdoptionStatus(models.TextChoices):
        UNAVAILABLE = "unavailable", "暂不可领养"
        AVAILABLE = "available", "待领养"
        ADOPTED = "adopted", "已领养"

    category = models.ForeignKey(
        AnimalCategory,
        on_delete=models.PROTECT,
        related_name="animals",
        verbose_name="动物分类",
    )
    name = models.CharField("动物名称", max_length=80, blank=True)
    gender = models.CharField(
        "性别", max_length=10, choices=Gender.choices, default=Gender.UNKNOWN
    )
    estimated_age = models.CharField("估算年龄", max_length=50, blank=True)
    health_status = models.CharField(
        "健康状态",
        max_length=20,
        choices=HealthStatus.choices,
        default=HealthStatus.UNKNOWN,
    )
    rescue_status = models.CharField(
        "救助状态",
        max_length=20,
        choices=RescueStatus.choices,
        default=RescueStatus.WAITING,
    )
    adoption_status = models.CharField(
        "领养状态",
        max_length=20,
        choices=AdoptionStatus.choices,
        default=AdoptionStatus.UNAVAILABLE,
    )
    campus = models.ForeignKey(
        "campuses.Campus",
        on_delete=models.PROTECT,
        related_name="animals",
        verbose_name="所属校区",
    )
    found_location = models.CharField("发现位置", max_length=255)
    description = models.TextField("情况说明")
    tags = models.ManyToManyField(
        "tags.Tag", related_name="animals", blank=True, verbose_name="标签"
    )
    is_published = models.BooleanField("公开展示", default=True)
    published_at = models.DateTimeField("发布时间", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "动物信息"
        verbose_name_plural = "动物信息"
        ordering = ("-published_at", "-created_at")
        indexes = [
            models.Index(
                fields=("is_published", "rescue_status", "-published_at"),
                name="animal_rescue_pub_idx",
            ),
            models.Index(
                fields=("category", "health_status", "campus"), name="animal_filter_idx"
            ),
        ]

    def __str__(self) -> str:
        return self.name or f"{self.category}·{self.found_location}"

    @property
    def cover_image(self) -> "AnimalImage | None":
        images = list(self.images.all())
        return next(
            (image for image in images if image.is_cover), images[0] if images else None
        )


class AnimalImage(models.Model):
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="images", verbose_name="动物"
    )
    image = models.ImageField(
        "图片", upload_to=animal_image_upload_to, validators=(validate_image_size,)
    )
    caption = models.CharField("说明", max_length=100, blank=True)
    is_cover = models.BooleanField("封面图", default=False)
    sort_order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        verbose_name = "动物图片"
        verbose_name_plural = "动物图片"
        ordering = ("sort_order", "id")

    def __str__(self) -> str:
        return f"{self.animal} 图片"


class RescueRequest(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="rescue_requests",
        verbose_name="申请人",
    )
    category = models.ForeignKey(
        AnimalCategory,
        on_delete=models.PROTECT,
        related_name="rescue_requests",
        verbose_name="动物分类",
    )
    animal_name = models.CharField("动物名称", max_length=80, blank=True)
    gender = models.CharField(
        "性别", max_length=10, choices=Gender.choices, default=Gender.UNKNOWN
    )
    health_status = models.CharField(
        "健康状态",
        max_length=20,
        choices=HealthStatus.choices,
        default=HealthStatus.UNKNOWN,
    )
    campus = models.ForeignKey(
        "campuses.Campus",
        on_delete=models.PROTECT,
        related_name="rescue_requests",
        verbose_name="所属校区",
    )
    found_location = models.CharField("发现位置", max_length=255)
    description = models.TextField("情况说明")
    contact = models.CharField("联系方式", max_length=100)
    status = models.CharField(
        "审核状态",
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
    )
    review_note = models.TextField("审核备注", blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewed_rescue_requests",
        null=True,
        blank=True,
        verbose_name="审核人",
    )
    reviewed_at = models.DateTimeField("审核时间", null=True, blank=True)
    approved_animal = models.OneToOneField(
        Animal,
        on_delete=models.SET_NULL,
        related_name="source_request",
        null=True,
        blank=True,
        verbose_name="生成的动物档案",
    )
    created_at = models.DateTimeField("申请时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "救助申请"
        verbose_name_plural = "救助申请"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("status", "-created_at"), name="rescue_review_idx")
        ]

    def __str__(self) -> str:
        return f"{self.applicant} - {self.animal_name or self.category.name}"


class RescueRequestImage(models.Model):
    rescue_request = models.ForeignKey(
        RescueRequest,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="救助申请",
    )
    image = models.ImageField(
        "图片", upload_to=rescue_image_upload_to, validators=(validate_image_size,)
    )
    sort_order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        verbose_name = "救助申请图片"
        verbose_name_plural = "救助申请图片"
        ordering = ("sort_order", "id")

    def __str__(self) -> str:
        return f"{self.rescue_request} 图片"
