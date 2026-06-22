from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "recipient", "business_type", "created_at", "read_at")
    list_filter = ("business_type", "read_at")
    search_fields = ("title", "content", "recipient__username")
    readonly_fields = ("created_at", "read_at")
