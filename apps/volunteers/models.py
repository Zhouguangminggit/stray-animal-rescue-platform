import uuid
from pathlib import Path

from django.conf import settings
from django.db import models

from apps.animals.models import ReviewStatus
from apps.core.validators import validate_document_size, validate_image_size


def volunteer_material_upload_to(instance: object, filename: str) -> str:
    extension = Path(filename).suffix.lower()
    return f"volunteers/materials/{uuid.uuid4().hex}{extension}"


def article_cover_upload_to(instance: object, filename: str) -> str:
    extension = Path(filename).suffix.lower() or ".jpg"
    return f"community/articles/{uuid.uuid4().hex}{extension}"


class VolunteerApplication(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="volunteer_applications",
        verbose_name="申请人",
    )
    intention = models.TextField("志愿意愿")
    skills = models.CharField("擅长技能", max_length=255)
    availability = models.CharField("可服务时间", max_length=255)
    experience = models.TextField("相关经验", blank=True)
    material = models.FileField(
        "申请材料",
        upload_to=volunteer_material_upload_to,
        blank=True,
        validators=(validate_document_size,),
    )
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
        related_name="reviewed_volunteer_applications",
        null=True,
        blank=True,
        verbose_name="审核人",
    )
    reviewed_at = models.DateTimeField("审核时间", null=True, blank=True)
    created_at = models.DateTimeField("申请时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "志愿者申请"
        verbose_name_plural = "志愿者申请"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("status", "-created_at"), name="volunteer_review_idx")
        ]

    def __str__(self) -> str:
        return f"{self.applicant} 的志愿者申请"


class VolunteerProfile(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "有效"
        INACTIVE = "inactive", "暂停"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="volunteer_profile",
        verbose_name="用户",
    )
    source_application = models.OneToOneField(
        VolunteerApplication,
        on_delete=models.SET_NULL,
        related_name="profile",
        null=True,
        blank=True,
        verbose_name="来源申请",
    )
    skills = models.CharField("擅长技能", max_length=255)
    availability = models.CharField("可服务时间", max_length=255)
    bio = models.TextField("志愿者简介", blank=True)
    status = models.CharField(
        "状态", max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    tags = models.ManyToManyField(
        "tags.Tag", related_name="volunteers", blank=True, verbose_name="标签"
    )
    joined_at = models.DateTimeField("加入时间", auto_now_add=True)

    class Meta:
        verbose_name = "志愿者档案"
        verbose_name_plural = "志愿者档案"
        ordering = ("-joined_at",)

    def __str__(self) -> str:
        return self.user.display_name


class CommunityArticle(models.Model):
    title = models.CharField("标题", max_length=150)
    summary = models.CharField("摘要", max_length=300)
    content = models.TextField("正文")
    cover = models.ImageField(
        "封面图",
        upload_to=article_cover_upload_to,
        blank=True,
        validators=(validate_image_size,),
    )
    tags = models.ManyToManyField(
        "tags.Tag", related_name="community_articles", blank=True, verbose_name="标签"
    )
    is_published = models.BooleanField("发布", default=True)
    published_at = models.DateTimeField("发布时间", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "社区文章"
        verbose_name_plural = "社区文章"
        ordering = ("-published_at", "-created_at")

    def __str__(self) -> str:
        return self.title


class CommunityPost(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="community_posts",
        verbose_name="作者",
    )
    title = models.CharField("标题", max_length=150)
    content = models.TextField("内容")
    is_hidden = models.BooleanField("已隐藏", default=False)
    created_at = models.DateTimeField("发布时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "用户帖子"
        verbose_name_plural = "用户帖子"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("is_hidden", "-created_at"), name="community_post_pub_idx"
            )
        ]

    def __str__(self) -> str:
        return self.title


class CommunityReport(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "待处理"
        RESOLVED = "resolved", "已处理"
        DISMISSED = "dismissed", "已驳回"

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="community_reports",
        verbose_name="举报人",
    )
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="被举报帖子",
    )
    reason = models.TextField("举报原因")
    status = models.CharField(
        "处理状态", max_length=20, choices=Status.choices, default=Status.PENDING
    )
    pending_marker = models.BooleanField(default=True, null=True, editable=False)
    resolution_note = models.TextField("处理说明", blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewed_community_reports",
        null=True,
        blank=True,
        verbose_name="处理人",
    )
    reviewed_at = models.DateTimeField("处理时间", null=True, blank=True)
    created_at = models.DateTimeField("举报时间", auto_now_add=True)

    class Meta:
        verbose_name = "社区举报"
        verbose_name_plural = "社区举报"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("reporter", "post", "pending_marker"),
                name="uniq_pending_reporter_post",
            )
        ]

    def __str__(self) -> str:
        return f"{self.reporter} 举报 {self.post}"
