from django.contrib import admin

from .models import Campus, School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "address")

    def has_add_permission(self, request) -> bool:
        return super().has_add_permission(request) and not School.objects.exists()


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "address", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "address")
    list_per_page = 20
