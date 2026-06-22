from django.contrib import admin

from .models import Poster


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "page",
        "slot",
        "sort_order",
        "is_active",
        "starts_at",
        "ends_at",
    )
    list_editable = ("sort_order", "is_active")
    list_filter = ("page", "slot", "is_active", "tags")
    search_fields = ("title", "subtitle")
    filter_horizontal = ("tags",)
