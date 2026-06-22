from django.db import models


class TagCategory(models.Model):
    name = models.CharField("分类名称", max_length=50, unique=True)
    sort_order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "标签分类"
        verbose_name_plural = "标签分类"
        ordering = ("sort_order", "id")

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    category = models.ForeignKey(
        TagCategory, on_delete=models.PROTECT, related_name="tags", verbose_name="分类"
    )
    name = models.CharField("标签名称", max_length=50)
    color = models.CharField("颜色", max_length=20, default="#66793a")
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签内容"
        constraints = [
            models.UniqueConstraint(
                fields=("category", "name"), name="uniq_tag_category_name"
            )
        ]
        ordering = ("category", "name")

    def __str__(self) -> str:
        return self.name
