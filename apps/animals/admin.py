from django.contrib import admin, messages
from django.http import HttpRequest

from .models import (
    Animal,
    AnimalCategory,
    AnimalImage,
    RescueRequest,
    RescueRequestImage,
    ReviewStatus,
)
from .services import InvalidReviewState, review_rescue_request


class AnimalImageInline(admin.TabularInline):
    model = AnimalImage
    extra = 1


@admin.register(AnimalCategory)
class AnimalCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name",)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "health_status",
        "rescue_status",
        "adoption_status",
        "campus",
        "is_published",
        "published_at",
    )
    list_filter = (
        "category",
        "health_status",
        "rescue_status",
        "adoption_status",
        "campus",
        "is_published",
    )
    search_fields = ("name", "found_location", "description")
    filter_horizontal = ("tags",)
    inlines = (AnimalImageInline,)
    list_per_page = 20


class RescueRequestImageInline(admin.TabularInline):
    model = RescueRequestImage
    extra = 0
    readonly_fields = ("image", "sort_order")
    can_delete = False


@admin.register(RescueRequest)
class RescueRequestAdmin(admin.ModelAdmin):
    list_display = (
        "animal_name",
        "category",
        "applicant",
        "campus",
        "health_status",
        "status",
        "created_at",
        "reviewed_at",
    )
    list_filter = ("status", "category", "health_status", "campus", "created_at")
    search_fields = (
        "animal_name",
        "found_location",
        "description",
        "applicant__username",
        "applicant__email",
    )
    readonly_fields = (
        "applicant",
        "status",
        "review_note",
        "reviewed_by",
        "reviewed_at",
        "approved_animal",
        "created_at",
        "updated_at",
    )
    inlines = (RescueRequestImageInline,)
    actions = ("approve_requests", "reject_requests")
    list_per_page = 20

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    @admin.action(description="通过所选救助申请")
    def approve_requests(self, request: HttpRequest, queryset) -> None:
        completed = self._review(request, queryset, ReviewStatus.APPROVED)
        self.message_user(request, f"已通过 {completed} 条救助申请。", messages.SUCCESS)

    @admin.action(description="驳回所选救助申请")
    def reject_requests(self, request: HttpRequest, queryset) -> None:
        completed = self._review(
            request, queryset, ReviewStatus.REJECTED, "后台审核驳回"
        )
        self.message_user(request, f"已驳回 {completed} 条救助申请。", messages.WARNING)

    @staticmethod
    def _review(request: HttpRequest, queryset, decision: str, note: str = "") -> int:
        completed = 0
        for request_id in queryset.values_list("pk", flat=True):
            try:
                review_rescue_request(
                    request_id=request_id,
                    reviewer=request.user,
                    decision=decision,
                    note=note,
                )
            except InvalidReviewState:
                continue
            completed += 1
        return completed
