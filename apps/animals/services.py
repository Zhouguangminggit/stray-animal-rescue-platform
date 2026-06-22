from dataclasses import dataclass
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.notifications.models import Notification
from apps.notifications.services import create_notification

from .models import Animal, AnimalImage, RescueRequest, ReviewStatus


class InvalidReviewState(ValueError):
    pass


@dataclass(frozen=True)
class ReviewResult:
    rescue_request: RescueRequest
    animal: Animal | None


@transaction.atomic
def review_rescue_request(
    *, request_id: int, reviewer: Any, decision: str, note: str = ""
) -> ReviewResult:
    rescue_request = (
        RescueRequest.objects.select_for_update()
        .select_related("category", "campus", "applicant")
        .get(pk=request_id)
    )
    if rescue_request.status != ReviewStatus.PENDING:
        raise InvalidReviewState("该救助申请已审核，不能重复操作。")
    if decision not in {ReviewStatus.APPROVED, ReviewStatus.REJECTED}:
        raise ValueError("审核结果必须为通过或驳回。")

    animal = None
    if decision == ReviewStatus.APPROVED:
        animal = Animal.objects.create(
            category=rescue_request.category,
            name=rescue_request.animal_name,
            gender=rescue_request.gender,
            health_status=rescue_request.health_status,
            campus=rescue_request.campus,
            found_location=rescue_request.found_location,
            description=rescue_request.description,
            rescue_status=Animal.RescueStatus.WAITING,
            is_published=True,
            published_at=timezone.now(),
        )
        AnimalImage.objects.bulk_create(
            [
                AnimalImage(
                    animal=animal,
                    image=item.image.name,
                    is_cover=index == 0,
                    sort_order=index,
                )
                for index, item in enumerate(rescue_request.images.all())
            ]
        )

    rescue_request.status = decision
    rescue_request.review_note = note.strip()
    rescue_request.reviewed_by = reviewer
    rescue_request.reviewed_at = timezone.now()
    rescue_request.approved_animal = animal
    rescue_request.save(
        update_fields=(
            "status",
            "review_note",
            "reviewed_by",
            "reviewed_at",
            "approved_animal",
            "updated_at",
        )
    )
    approved = decision == ReviewStatus.APPROVED
    result_label = "通过" if approved else "驳回"
    create_notification(
        recipient=rescue_request.applicant,
        business_type=Notification.BusinessType.RESCUE,
        title="救助申请审核结果",
        content=f"您的救助申请已{result_label}。{rescue_request.review_note}",
        related_app="animals",
        related_object_id=rescue_request.pk,
    )
    return ReviewResult(rescue_request=rescue_request, animal=animal)
