from django.conf import settings
from django.db import models

from apps.animals.models import ReviewStatus


class AdoptionApplication(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="adoption_applications",
        verbose_name="申请人",
    )
    animal = models.ForeignKey(
        "animals.Animal",
        on_delete=models.PROTECT,
        related_name="adoption_applications",
        verbose_name="申请动物",
    )
    motivation = models.TextField("领养原因")
    housing = models.CharField("居住条件", max_length=255)
    experience = models.TextField("养宠经验", blank=True)
    contact = models.CharField("联系方式", max_length=100)
    status = models.CharField(
        "审核状态",
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
    )
    pending_marker = models.BooleanField(default=True, null=True, editable=False)
    review_note = models.TextField("审核备注", blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewed_adoption_applications",
        null=True,
        blank=True,
        verbose_name="审核人",
    )
    reviewed_at = models.DateTimeField("审核时间", null=True, blank=True)
    created_at = models.DateTimeField("申请时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "领养申请"
        verbose_name_plural = "领养申请"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("applicant", "animal", "pending_marker"),
                name="uniq_pending_adoption_user_animal",
            )
        ]
        indexes = [
            models.Index(fields=("status", "-created_at"), name="adoption_review_idx")
        ]

    def __str__(self) -> str:
        return f"{self.applicant} 申请领养 {self.animal}"


class AdoptionRelationship(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "有效"
        ENDED = "ended", "已终止"
        CANCELLED = "cancelled", "已撤销"

    application = models.OneToOneField(
        AdoptionApplication,
        on_delete=models.PROTECT,
        related_name="relationship",
        verbose_name="领养申请",
    )
    adopter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="adoption_relationships",
        verbose_name="领养人",
    )
    animal = models.ForeignKey(
        "animals.Animal",
        on_delete=models.PROTECT,
        related_name="adoption_relationships",
        verbose_name="领养动物",
    )
    status = models.CharField(
        "关系状态", max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    active_marker = models.BooleanField(default=True, null=True, editable=False)
    started_at = models.DateTimeField("领养开始时间")
    ended_at = models.DateTimeField("终止时间", null=True, blank=True)
    end_note = models.TextField("终止说明", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "领养关系"
        verbose_name_plural = "领养关系"
        ordering = ("-started_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("animal", "active_marker"), name="uniq_active_adoption_animal"
            )
        ]
        indexes = [
            models.Index(fields=("adopter", "status"), name="adoption_user_status_idx")
        ]

    def __str__(self) -> str:
        return f"{self.adopter} - {self.animal}"
