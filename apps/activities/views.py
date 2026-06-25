from typing import Any, cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.faqs.models import FAQModule, faqs_for

from .models import Activity, Participation
from .services import ActivityError, cancel_participation, register_activity


def activity_list(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "activities/list.html",
        {
            "page_obj": Paginator(
                Activity.objects.exclude(status=Activity.Status.DRAFT).select_related(
                    "campus"
                ),
                12,
            ).get_page(request.GET.get("page")),
            "module_stats": {
                "open": Activity.objects.filter(status=Activity.Status.OPEN).count(),
                "upcoming": Activity.objects.exclude(
                    status__in=(Activity.Status.DRAFT, Activity.Status.CANCELLED)
                )
                .filter(starts_at__gte=timezone.now())
                .count(),
                "registered": Participation.objects.filter(
                    status=Participation.Status.REGISTERED
                ).count(),
                "capacity": Activity.objects.filter(
                    status=Activity.Status.OPEN
                ).aggregate(total=Sum("capacity"))["total"]
                or 0,
            },
            "campus_snapshots": Activity.objects.exclude(
                status__in=(Activity.Status.DRAFT, Activity.Status.CANCELLED)
            )
            .values("campus__name")
            .annotate(
                total=Count("id"),
                registered=Count(
                    "participations",
                    filter=Q(participations__status=Participation.Status.REGISTERED),
                ),
            )
            .order_by("-total", "campus__name")[:3],
            "faqs": faqs_for(FAQModule.ACTIVITY),
        },
    )


def activity_detail(request: HttpRequest, pk: int) -> HttpResponse:
    return render(
        request,
        "activities/detail.html",
        {
            "activity": get_object_or_404(
                Activity.objects.select_related("campus"), pk=pk
            )
        },
    )


@require_POST
@login_required
def register(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        register_activity(user=request.user, activity_id=pk)
    except ActivityError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "活动报名成功。")
    return redirect("activities:detail", pk=pk)


@require_POST
@login_required
def cancel(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        cancel_participation(participation_id=pk, user=request.user)
    except ActivityError as exc:
        messages.error(request, str(exc))
    return redirect("activities:mine")


@login_required
def mine(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "activities/mine.html",
        {
            "participations": Participation.objects.filter(
                user=cast(Any, request.user)
            ).select_related("activity")
        },
    )
