from typing import Any

from django.db import transaction
from django.utils import timezone

from .models import Activity, Participation


class ActivityError(ValueError):
    pass


@transaction.atomic
def register_activity(*, user: Any, activity_id: int) -> Participation:
    activity = Activity.objects.select_for_update().get(pk=activity_id)
    now = timezone.now()
    if activity.status != Activity.Status.OPEN or not (
        activity.registration_starts_at <= now <= activity.registration_ends_at
    ):
        raise ActivityError("该活动当前不可报名。")
    if Participation.objects.filter(
        user=user, activity=activity, status=Participation.Status.REGISTERED
    ).exists():
        raise ActivityError("您已报名该活动。")
    if (
        Participation.objects.filter(
            activity=activity, status=Participation.Status.REGISTERED
        ).count()
        >= activity.capacity
    ):
        raise ActivityError("该活动名额已满。")
    return Participation.objects.create(user=user, activity=activity)


@transaction.atomic
def cancel_participation(*, participation_id: int, user: Any) -> Participation:
    participation = Participation.objects.select_for_update().get(
        pk=participation_id, user=user
    )
    if participation.status != Participation.Status.REGISTERED:
        raise ActivityError("该报名已取消。")
    participation.status = Participation.Status.CANCELLED
    participation.active_marker = None
    participation.cancelled_at = timezone.now()
    participation.save(update_fields=("status", "active_marker", "cancelled_at"))
    return participation
