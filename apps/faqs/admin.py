from django.contrib import admin

from .models import FAQ, FAQCategory


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "module", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("module", "is_active")
    search_fields = ("name",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("category__module", "category", "is_active")
    search_fields = ("question", "answer")
