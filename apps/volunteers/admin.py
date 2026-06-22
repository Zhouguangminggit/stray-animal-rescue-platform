from django.contrib import admin, messages

from apps.animals.models import ReviewStatus

from .models import (
    CommunityArticle,
    CommunityPost,
    CommunityReport,
    VolunteerApplication,
    VolunteerProfile,
)
from .services import (
    CommunityWorkflowError,
    resolve_community_report,
    review_volunteer_application,
)


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant", "skills", "availability", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("applicant__username", "skills", "intention")
    readonly_fields = (
        "applicant",
        "status",
        "review_note",
        "reviewed_by",
        "reviewed_at",
        "created_at",
        "updated_at",
    )
    actions = ("approve", "reject")

    def has_add_permission(self, request):
        return False

    @admin.action(description="通过所选志愿者申请")
    def approve(self, request, queryset):
        self._review(request, queryset, ReviewStatus.APPROVED)

    @admin.action(description="驳回所选志愿者申请")
    def reject(self, request, queryset):
        self._review(request, queryset, ReviewStatus.REJECTED, "后台审核驳回")

    def _review(self, request, queryset, decision, note=""):
        completed = 0
        for pk in queryset.values_list("pk", flat=True):
            try:
                review_volunteer_application(
                    application_id=pk,
                    reviewer=request.user,
                    decision=decision,
                    note=note,
                )
            except CommunityWorkflowError:
                continue
            completed += 1
        self.message_user(request, f"已处理 {completed} 条申请。", messages.SUCCESS)


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "skills", "availability", "status", "joined_at")
    list_filter = ("status", "tags")
    search_fields = ("user__username", "user__email", "skills")
    filter_horizontal = ("tags",)


@admin.register(CommunityArticle)
class CommunityArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at", "updated_at")
    list_filter = ("is_published", "tags")
    search_fields = ("title", "summary", "content")
    filter_horizontal = ("tags",)


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_hidden", "created_at")
    list_filter = ("is_hidden", "created_at")
    search_fields = ("title", "content", "author__username")
    readonly_fields = ("author", "title", "content", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False


@admin.register(CommunityReport)
class CommunityReportAdmin(admin.ModelAdmin):
    list_display = ("post", "reporter", "status", "created_at", "reviewed_at")
    list_filter = ("status", "created_at")
    search_fields = ("post__title", "reporter__username", "reason")
    readonly_fields = (
        "reporter",
        "post",
        "reason",
        "status",
        "resolution_note",
        "reviewed_by",
        "reviewed_at",
        "created_at",
    )
    actions = ("hide_content", "keep_content")

    def has_add_permission(self, request):
        return False

    @admin.action(description="核实举报并隐藏内容")
    def hide_content(self, request, queryset):
        self._resolve(request, queryset, "hide")

    @admin.action(description="驳回举报并保留内容")
    def keep_content(self, request, queryset):
        self._resolve(request, queryset, "keep")

    def _resolve(self, request, queryset, decision):
        completed = 0
        for pk in queryset.values_list("pk", flat=True):
            try:
                resolve_community_report(
                    report_id=pk, reviewer=request.user, decision=decision
                )
            except CommunityWorkflowError:
                continue
            completed += 1
        self.message_user(request, f"已处理 {completed} 条举报。", messages.SUCCESS)
