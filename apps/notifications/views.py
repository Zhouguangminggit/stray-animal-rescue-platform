from typing import Any, cast

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notification_list(request: HttpRequest) -> HttpResponse:
    page = Paginator(
        Notification.objects.filter(recipient=cast(Any, request.user)), 20
    ).get_page(request.GET.get("page"))
    return render(request, "notifications/list.html", {"page_obj": page})


@login_required
def notification_detail(request: HttpRequest, pk: int) -> HttpResponse:
    notice = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if notice.read_at is None:
        notice.read_at = timezone.now()
        notice.save(update_fields=("read_at",))
    return render(request, "notifications/detail.html", {"notification": notice})


@require_POST
@login_required
def mark_read(request: HttpRequest, pk: int) -> HttpResponse:
    notice = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if notice.read_at is None:
        notice.read_at = timezone.now()
        notice.save(update_fields=("read_at",))
    return redirect("notifications:list")
