from django.db import models


class FAQModule(models.TextChoices):
    RESCUE = "rescue", "救助信息"
    ADOPTION = "adoption", "领养中心"
    VOLUNTEER = "volunteer", "志愿者社区"
    DONATION = "donation", "爱心捐赠"
    ACTIVITY = "activity", "校园活动"


class FAQCategory(models.Model):
    module = models.CharField("所属模块", max_length=20, choices=FAQModule.choices)
    name = models.CharField("分类名称", max_length=100)
    sort_order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "FAQ 分类"
        verbose_name_plural = "FAQ 分类"
        ordering = ("module", "sort_order", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("module", "name"), name="uniq_faq_module_category"
            )
        ]

    def __str__(self) -> str:
        return f"{self.get_module_display()} - {self.name}"


class FAQ(models.Model):
    category = models.ForeignKey(
        FAQCategory, on_delete=models.CASCADE, related_name="faqs", verbose_name="分类"
    )
    question = models.CharField("问题", max_length=255)
    answer = models.TextField("答案")
    sort_order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("启用", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ 问题"
        verbose_name_plural = "FAQ 问题"
        ordering = ("category", "sort_order", "id")

    def __str__(self) -> str:
        return self.question


def faqs_for(module: str):
    return FAQ.objects.filter(
        is_active=True, category__is_active=True, category__module=module
    ).select_related("category")
