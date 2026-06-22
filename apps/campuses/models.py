from django.core.exceptions import ValidationError
from django.db import models


class School(models.Model):
    name = models.CharField("学校名称", max_length=100, unique=True)
    address = models.CharField("学校地址", max_length=255, blank=True)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "学校"
        verbose_name_plural = "学校管理"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if School.objects.exclude(pk=self.pk).exists():
            raise ValidationError("系统仅允许配置一所学校。")


class Campus(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.PROTECT, related_name="campuses", verbose_name="学校"
    )
    name = models.CharField("校区名称", max_length=100)
    address = models.CharField("校区地址", max_length=255, blank=True)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "校区"
        verbose_name_plural = "校区管理"
        constraints = [
            models.UniqueConstraint(
                fields=("school", "name"), name="uniq_campus_school_name"
            )
        ]
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
