from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.animals.models import ReviewStatus
from apps.notifications.models import Notification
from apps.notifications.services import create_notification

from .models import CommunityReport, VolunteerApplication, VolunteerProfile


class CommunityWorkflowError(ValueError):
    pass


@transaction.atomic
def review_volunteer_application(
    *, application_id: int, reviewer: Any, decision: str, note: str = ""
) -> VolunteerApplication:
    application = (
        VolunteerApplication.objects.select_for_update()
        .select_related("applicant")
        .get(pk=application_id)
    )
    if application.status != ReviewStatus.PENDING:
        raise CommunityWorkflowError("该志愿者申请已审核。")
    if decision not in {ReviewStatus.APPROVED, ReviewStatus.REJECTED}:
        raise ValueError("审核结果无效。")
    if decision == ReviewStatus.APPROVED:
        VolunteerProfile.objects.update_or_create(
            user=application.applicant,
            defaults={
                "source_application": application,
                "skills": application.skills,
                "availability": application.availability,
                "bio": application.experience,
                "status": VolunteerProfile.Status.ACTIVE,
            },
        )
    application.status = decision
    application.review_note = note.strip()
    application.reviewed_by = reviewer
    application.reviewed_at = timezone.now()
    application.save(
        update_fields=(
            "status",
            "review_note",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        )
    )
    label = "通过" if decision == ReviewStatus.APPROVED else "驳回"
    create_notification(
        recipient=application.applicant,
        business_type=Notification.BusinessType.VOLUNTEER,
        title="志愿者申请审核结果",
        content=f"您的志愿者申请已{label}。{application.review_note}",
        related_app="volunteers",
        related_object_id=application.pk,
    )
    return application


@transaction.atomic
def resolve_community_report(
    *, report_id: int, reviewer: Any, decision: str, note: str = ""
) -> CommunityReport:
    report = (
        CommunityReport.objects.select_for_update()
        .select_related("post", "post__author", "reporter")
        .get(pk=report_id)
    )
    if report.status != CommunityReport.Status.PENDING:
        raise CommunityWorkflowError("该举报已处理。")
    if decision not in {"hide", "keep"}:
        raise ValueError("举报处理结果无效。")
    if decision == "hide":
        report.post.is_hidden = True
        report.post.save(update_fields=("is_hidden", "updated_at"))
        report.status = CommunityReport.Status.RESOLVED
        reporter_text = "举报已核实，内容已隐藏"
        author_text = f"您发布的「{report.post}」因举报核实已隐藏。"
    else:
        report.status = CommunityReport.Status.DISMISSED
        reporter_text = "举报未核实，内容继续保留"
        author_text = f"您发布的「{report.post}」举报已处理，内容继续保留。"
    report.pending_marker = None
    report.resolution_note = note.strip()
    report.reviewed_by = reviewer
    report.reviewed_at = timezone.now()
    report.save(
        update_fields=(
            "status",
            "pending_marker",
            "resolution_note",
            "reviewed_by",
            "reviewed_at",
        )
    )
    for recipient, content in (
        (report.reporter, reporter_text),
        (report.post.author, author_text),
    ):
        create_notification(
            recipient=recipient,
            business_type=Notification.BusinessType.REPORT,
            title="社区举报处理结果",
            content=f"{content}。{report.resolution_note}",
            related_app="volunteers",
            related_object_id=report.pk,
        )
    return report
