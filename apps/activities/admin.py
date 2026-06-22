from django.contrib import admin

from .models import Activity, Participation


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "campus", "status", "starts_at", "capacity")
    list_filter = ("status", "campus", "tags")
    search_fields = ("title", "summary", "location")
    filter_horizontal = ("tags",)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("user", "activity", "status", "registered_at", "cancelled_at")
    list_filter = ("status", "activity")
    readonly_fields = ("user", "activity", "status", "registered_at", "cancelled_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
