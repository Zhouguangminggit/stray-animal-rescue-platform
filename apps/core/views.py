from django.db import connection
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from apps.activities.models import Activity
from apps.adoptions.models import AdoptionRelationship
from apps.animals.models import Animal
from apps.donations.models import DonationItem, DonationProject
from apps.posters.models import Poster
from apps.volunteers.models import VolunteerProfile


@require_GET
def health(request: HttpRequest) -> JsonResponse:
    """Report whether Django can reach its configured database."""
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({"status": "unhealthy"}, status=503)
    return JsonResponse({"status": "healthy"})


@require_GET
def home(request: HttpRequest):
    latest_animals = (
        Animal.objects.filter(is_published=True)
        .select_related("category", "campus")
        .prefetch_related("images")[:6]
    )
    latest_activities = Activity.objects.exclude(
        status__in=(Activity.Status.DRAFT, Activity.Status.CANCELLED)
    ).select_related("campus")[:3]
    urgent_items = (
        DonationItem.objects.filter(project__status=DonationProject.Status.OPEN)
        .select_related("project")
        .prefetch_related("pledges")[:4]
    )
    return render(
        request,
        "core/home.html",
        {
            "banners": Poster.active_for(
                page=Poster.Page.HOME, slot=Poster.Slot.BANNER
            ),
            "quick_entries": Poster.active_for(
                page=Poster.Page.HOME, slot=Poster.Slot.QUICK_ENTRY
            ),
            "welfare_posters": Poster.active_for(
                page=Poster.Page.HOME, slot=Poster.Slot.PUBLIC_WELFARE
            ),
            "latest_animals": latest_animals,
            "latest_activities": latest_activities,
            "urgent_items": urgent_items,
            "stats": {
                "rescued": Animal.objects.filter(
                    rescue_status=Animal.RescueStatus.RESCUED
                ).count(),
                "adopted": AdoptionRelationship.objects.filter(
                    status=AdoptionRelationship.Status.ACTIVE
                ).count(),
                "volunteers": VolunteerProfile.objects.filter(
                    status=VolunteerProfile.Status.ACTIVE
                ).count(),
                "donations": DonationProject.objects.filter(
                    status=DonationProject.Status.OPEN
                ).count(),
            },
        },
    )
