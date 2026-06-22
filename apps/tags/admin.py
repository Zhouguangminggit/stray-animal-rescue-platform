from django.contrib import admin

from .models import Tag, TagCategory


@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name",)
    list_per_page = 20


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "color", "is_active")
    list_editable = ("color", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    list_per_page = 20
