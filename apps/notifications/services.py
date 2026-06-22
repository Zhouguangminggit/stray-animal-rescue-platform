from typing import Any

from .models import Notification


def create_notification(
    *,
    recipient: Any,
    title: str,
    content: str,
    business_type: str = Notification.BusinessType.SYSTEM,
    related_app: str = "",
    related_object_id: int | None = None,
) -> Notification:
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        content=content,
        business_type=business_type,
        related_app=related_app,
        related_object_id=related_object_id,
    )
