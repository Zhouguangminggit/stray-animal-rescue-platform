from typing import Any, cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.faqs.models import FAQModule, faqs_for

from .models import DonationItem, DonationProject, Pledge
from .services import DonationError, create_pledge


def project_list(request: HttpRequest) -> HttpResponse:
    page = Paginator(
        DonationProject.objects.exclude(
            status=DonationProject.Status.DRAFT
        ).prefetch_related("items", "tags"),
        12,
    ).get_page(request.GET.get("page"))
    return render(
        request,
        "donations/list.html",
        {
            "page_obj": page,
            "module_stats": {
                "open_projects": DonationProject.objects.filter(
                    status=DonationProject.Status.OPEN
                ).count(),
                "items": DonationItem.objects.filter(
                    project__status=DonationProject.Status.OPEN
                ).count(),
                "pledged_quantity": Pledge.objects.filter(
                    status__in=(Pledge.Status.PLEDGED, Pledge.Status.CONFIRMED)
                ).aggregate(total=Sum("quantity"))["total"]
                or 0,
                "supporters": Pledge.objects.values("user").distinct().count(),
            },
            "urgent_items": DonationItem.objects.filter(
                project__status=DonationProject.Status.OPEN
            )
            .select_related("project")
            .annotate(
                pledge_count=Count(
                    "pledges",
                    filter=Q(
                        pledges__status__in=(
                            Pledge.Status.PLEDGED,
                            Pledge.Status.CONFIRMED,
                        )
                    ),
                )
            )[:4],
            "faqs": faqs_for(FAQModule.DONATION),
        },
    )


def project_detail(request: HttpRequest, pk: int) -> HttpResponse:
    project = get_object_or_404(
        DonationProject.objects.prefetch_related("items__pledges", "tags"), pk=pk
    )
    return render(request, "donations/detail.html", {"project": project})


@require_POST
@login_required
def pledge(request: HttpRequest, item_id: int) -> HttpResponse:
    item = get_object_or_404(DonationItem, pk=item_id)
    try:
        quantity = int(request.POST.get("quantity", "0"))
        create_pledge(
            user=request.user,
            item_id=item.pk,
            quantity=quantity,
            note=request.POST.get("note", ""),
        )
    except (ValueError, DonationError) as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "物资认捐已提交。")
    return redirect("donations:detail", pk=item.project_id)


@login_required
def mine(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "donations/mine.html",
        {
            "pledges": Pledge.objects.filter(
                user=cast(Any, request.user)
            ).select_related("item", "item__project")
        },
    )
