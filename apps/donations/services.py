from typing import Any

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from .models import DonationItem, DonationProject, Pledge


class DonationError(ValueError):
    pass


@transaction.atomic
def create_pledge(*, user: Any, item_id: int, quantity: int, note: str = "") -> Pledge:
    item = (
        DonationItem.objects.select_for_update()
        .select_related("project")
        .get(pk=item_id)
    )
    now = timezone.now()
    if item.project.status != DonationProject.Status.OPEN or not (
        item.project.starts_at <= now <= item.project.ends_at
    ):
        raise DonationError("该捐赠项目当前不可参与。")
    if quantity <= 0:
        raise DonationError("认捐数量必须大于 0。")
    pledged = (
        Pledge.objects.filter(
            item=item, status__in=(Pledge.Status.PLEDGED, Pledge.Status.CONFIRMED)
        ).aggregate(total=Sum("quantity"))["total"]
        or 0
    )
    if quantity > item.required_quantity - pledged:
        raise DonationError("认捐数量超过当前剩余需求。")
    return Pledge.objects.create(
        user=user, item=item, quantity=quantity, note=note.strip()
    )


@transaction.atomic
def update_pledge_status(*, pledge_id: int, status: str) -> Pledge:
    pledge = Pledge.objects.select_for_update().get(pk=pledge_id)
    if pledge.status != Pledge.Status.PLEDGED:
        raise DonationError("该认捐记录已处理。")
    if status not in {Pledge.Status.CONFIRMED, Pledge.Status.CANCELLED}:
        raise ValueError("认捐状态无效。")
    pledge.status = status
    pledge.save(update_fields=("status", "updated_at"))
    return pledge
