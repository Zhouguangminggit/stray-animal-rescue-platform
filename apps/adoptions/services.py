from dataclasses import dataclass
from typing import Any

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.animals.models import Animal, ReviewStatus
from apps.notifications.models import Notification
from apps.notifications.services import create_notification

from .models import AdoptionApplication, AdoptionRelationship

MAX_ACTIVE_ADOPTIONS = 3


class AdoptionError(ValueError):
    pass


class InvalidAdoptionState(AdoptionError):
    pass


class AdoptionLimitReached(AdoptionError):
    pass


@dataclass(frozen=True)
class AdoptionReviewResult:
    application: AdoptionApplication
    relationship: AdoptionRelationship | None


@transaction.atomic
def submit_adoption_application(
    *,
    applicant: Any,
    animal_id: int,
    motivation: str,
    housing: str,
    experience: str,
    contact: str,
) -> AdoptionApplication:
    animal = Animal.objects.select_for_update().get(pk=animal_id, is_published=True)
    if animal.adoption_status != Animal.AdoptionStatus.AVAILABLE:
        raise InvalidAdoptionState("该动物当前不可申请领养。")
    if AdoptionApplication.objects.filter(
        applicant=applicant, animal=animal, status=ReviewStatus.PENDING
    ).exists():
        raise InvalidAdoptionState("您已有该动物的待审核申请。")
    if (
        AdoptionRelationship.objects.filter(
            adopter=applicant, status=AdoptionRelationship.Status.ACTIVE
        ).count()
        >= MAX_ACTIVE_ADOPTIONS
    ):
        raise AdoptionLimitReached("您当前有效领养数量已达 3 只。")
    try:
        return AdoptionApplication.objects.create(
            applicant=applicant,
            animal=animal,
            motivation=motivation.strip(),
            housing=housing.strip(),
            experience=experience.strip(),
            contact=contact.strip(),
        )
    except IntegrityError as exc:
        raise InvalidAdoptionState("您已有该动物的待审核申请。") from exc


@transaction.atomic
def review_adoption_application(
    *, application_id: int, reviewer: Any, decision: str, note: str = ""
) -> AdoptionReviewResult:
    application = (
        AdoptionApplication.objects.select_for_update()
        .select_related("animal", "applicant")
        .get(pk=application_id)
    )
    if application.status != ReviewStatus.PENDING:
        raise InvalidAdoptionState("该领养申请已审核，不能重复操作。")
    if decision not in {ReviewStatus.APPROVED, ReviewStatus.REJECTED}:
        raise ValueError("审核结果必须为通过或驳回。")

    animal = Animal.objects.select_for_update().get(pk=application.animal_id)
    relationship = None
    if decision == ReviewStatus.APPROVED:
        if animal.adoption_status != Animal.AdoptionStatus.AVAILABLE:
            raise InvalidAdoptionState("该动物已不可领养。")
        active_count = (
            AdoptionRelationship.objects.select_for_update()
            .filter(
                adopter=application.applicant, status=AdoptionRelationship.Status.ACTIVE
            )
            .count()
        )
        if active_count >= MAX_ACTIVE_ADOPTIONS:
            raise AdoptionLimitReached("申请人当前有效领养数量已达 3 只。")
        relationship = AdoptionRelationship.objects.create(
            application=application,
            adopter=application.applicant,
            animal=animal,
            started_at=timezone.now(),
        )
        animal.adoption_status = Animal.AdoptionStatus.ADOPTED
        animal.save(update_fields=("adoption_status", "updated_at"))

    application.status = decision
    application.pending_marker = None
    application.review_note = note.strip()
    application.reviewed_by = reviewer
    application.reviewed_at = timezone.now()
    application.save(
        update_fields=(
            "status",
            "pending_marker",
            "review_note",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        )
    )
    result_label = "通过" if decision == ReviewStatus.APPROVED else "驳回"
    create_notification(
        recipient=application.applicant,
        business_type=Notification.BusinessType.ADOPTION,
        title="领养申请审核结果",
        content=f"您对「{animal}」的领养申请已{result_label}。{application.review_note}",
        related_app="adoptions",
        related_object_id=application.pk,
    )

    if decision == ReviewStatus.APPROVED:
        competing = list(
            AdoptionApplication.objects.select_for_update()
            .filter(animal=animal, status=ReviewStatus.PENDING)
            .exclude(pk=application.pk)
            .select_related("applicant")
        )
        for item in competing:
            item.status = ReviewStatus.REJECTED
            item.pending_marker = None
            item.review_note = "该动物已完成领养"
            item.reviewed_by = reviewer
            item.reviewed_at = timezone.now()
            item.save(
                update_fields=(
                    "status",
                    "pending_marker",
                    "review_note",
                    "reviewed_by",
                    "reviewed_at",
                    "updated_at",
                )
            )
            create_notification(
                recipient=item.applicant,
                business_type=Notification.BusinessType.ADOPTION,
                title="领养申请审核结果",
                content=f"您对「{animal}」的领养申请已驳回：该动物已完成领养。",
                related_app="adoptions",
                related_object_id=item.pk,
            )
    return AdoptionReviewResult(application=application, relationship=relationship)


@transaction.atomic
def end_adoption_relationship(
    *, relationship_id: int, note: str = ""
) -> AdoptionRelationship:
    relationship = (
        AdoptionRelationship.objects.select_for_update()
        .select_related("animal", "adopter")
        .get(pk=relationship_id)
    )
    if relationship.status != AdoptionRelationship.Status.ACTIVE:
        raise InvalidAdoptionState("该领养关系已终止。")
    animal = Animal.objects.select_for_update().get(pk=relationship.animal_id)
    relationship.status = AdoptionRelationship.Status.ENDED
    relationship.active_marker = None
    relationship.ended_at = timezone.now()
    relationship.end_note = note.strip()
    relationship.save(update_fields=("status", "active_marker", "ended_at", "end_note"))
    animal.adoption_status = Animal.AdoptionStatus.AVAILABLE
    animal.save(update_fields=("adoption_status", "updated_at"))
    create_notification(
        recipient=relationship.adopter,
        business_type=Notification.BusinessType.ADOPTION,
        title="领养关系已终止",
        content=f"您与「{animal}」的领养关系已终止。{relationship.end_note}",
        related_app="adoptions",
        related_object_id=relationship.pk,
    )
    return relationship
