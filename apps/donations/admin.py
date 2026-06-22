from django.contrib import admin

from .models import DonationItem, DonationProject, Pledge
from .services import DonationError, update_pledge_status


class DonationItemInline(admin.TabularInline):
    model = DonationItem
    extra = 1


@admin.register(DonationProject)
class DonationProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "starts_at", "ends_at")
    list_filter = ("status", "tags")
    search_fields = ("title", "summary")
    filter_horizontal = ("tags",)
    inlines = (DonationItemInline,)


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "quantity", "status", "created_at")
    list_filter = ("status", "item__project")
    readonly_fields = (
        "user",
        "item",
        "quantity",
        "note",
        "status",
        "created_at",
        "updated_at",
    )
    actions = ("confirm", "cancel")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="确认所选物资已交付")
    def confirm(self, request, queryset):
        self._update(queryset, Pledge.Status.CONFIRMED)

    @admin.action(description="取消所选认捐")
    def cancel(self, request, queryset):
        self._update(queryset, Pledge.Status.CANCELLED)

    @staticmethod
    def _update(queryset, status):
        for pk in queryset.values_list("pk", flat=True):
            try:
                update_pledge_status(pledge_id=pk, status=status)
            except DonationError:
                continue
