from django.contrib import admin, messages
from django.http import HttpRequest

from apps.animals.models import ReviewStatus

from .models import AdoptionApplication, AdoptionRelationship
from .services import (
    AdoptionError,
    end_adoption_relationship,
    review_adoption_application,
)


@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "applicant",
        "animal",
        "status",
        "created_at",
        "reviewed_by",
        "reviewed_at",
    )
    list_filter = ("status", "animal__category", "animal__campus", "created_at")
    search_fields = (
        "applicant__username",
        "applicant__email",
        "animal__name",
        "contact",
    )
    readonly_fields = (
        "applicant",
        "animal",
        "motivation",
        "housing",
        "experience",
        "contact",
        "status",
        "review_note",
        "reviewed_by",
        "reviewed_at",
        "created_at",
        "updated_at",
    )
    actions = ("approve_applications", "reject_applications")
    list_per_page = 20

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    @admin.action(description="通过所选领养申请")
    def approve_applications(self, request: HttpRequest, queryset) -> None:
        completed = self._review(request, queryset, ReviewStatus.APPROVED)
        self.message_user(request, f"已通过 {completed} 条领养申请。", messages.SUCCESS)

    @admin.action(description="驳回所选领养申请")
    def reject_applications(self, request: HttpRequest, queryset) -> None:
        completed = self._review(
            request, queryset, ReviewStatus.REJECTED, "后台审核驳回"
        )
        self.message_user(request, f"已驳回 {completed} 条领养申请。", messages.WARNING)

    @staticmethod
    def _review(request: HttpRequest, queryset, decision: str, note: str = "") -> int:
        completed = 0
        for application_id in queryset.values_list("pk", flat=True):
            try:
                review_adoption_application(
                    application_id=application_id,
                    reviewer=request.user,
                    decision=decision,
                    note=note,
                )
            except AdoptionError:
                continue
            completed += 1
        return completed


@admin.register(AdoptionRelationship)
class AdoptionRelationshipAdmin(admin.ModelAdmin):
    list_display = ("adopter", "animal", "status", "started_at", "ended_at")
    list_filter = ("status", "animal__category", "animal__campus", "started_at")
    search_fields = ("adopter__username", "adopter__email", "animal__name")
    readonly_fields = (
        "application",
        "adopter",
        "animal",
        "status",
        "started_at",
        "ended_at",
        "end_note",
        "created_at",
    )
    actions = ("end_relationships",)
    list_per_page = 20

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    @admin.action(description="终止所选有效领养关系")
    def end_relationships(self, request: HttpRequest, queryset) -> None:
        completed = 0
        for relationship_id in queryset.values_list("pk", flat=True):
            try:
                end_adoption_relationship(
                    relationship_id=relationship_id, note="后台终止"
                )
            except AdoptionError:
                continue
            completed += 1
        self.message_user(request, f"已终止 {completed} 条领养关系。", messages.WARNING)
