from typing import Any, cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.animals.models import Animal, AnimalCategory
from apps.campuses.models import Campus
from apps.faqs.models import FAQModule, faqs_for

from .forms import AdoptionApplicationForm
from .models import AdoptionApplication, AdoptionRelationship
from .services import AdoptionError, submit_adoption_application


def adoption_list(request: HttpRequest) -> HttpResponse:
    animals = (
        Animal.objects.filter(
            is_published=True,
            adoption_status__in=(
                Animal.AdoptionStatus.AVAILABLE,
                Animal.AdoptionStatus.ADOPTED,
            ),
        )
        .select_related("category", "campus")
        .prefetch_related("images", "tags")
    )
    category = request.GET.get("category", "")
    health = request.GET.get("health", "")
    campus = request.GET.get("campus", "")
    status = request.GET.get("status", "")
    if category.isdigit():
        animals = animals.filter(category_id=int(category))
    if health:
        animals = animals.filter(health_status=health)
    if campus.isdigit():
        animals = animals.filter(campus_id=int(campus))
    if status:
        animals = animals.filter(adoption_status=status)
    page = Paginator(animals, 12).get_page(request.GET.get("page"))
    return render(
        request,
        "adoptions/list.html",
        {
            "page_obj": page,
            "categories": AnimalCategory.objects.filter(is_active=True),
            "campuses": Campus.objects.filter(is_active=True),
            "health_choices": Animal._meta.get_field("health_status").choices,
            "status_choices": (
                (Animal.AdoptionStatus.AVAILABLE, "待领养"),
                (Animal.AdoptionStatus.ADOPTED, "已领养"),
            ),
            "module_stats": {
                "available": Animal.objects.filter(
                    is_published=True,
                    adoption_status=Animal.AdoptionStatus.AVAILABLE,
                ).count(),
                "adopted": Animal.objects.filter(
                    is_published=True,
                    adoption_status=Animal.AdoptionStatus.ADOPTED,
                ).count(),
                "relationships": AdoptionRelationship.objects.filter(
                    status=AdoptionRelationship.Status.ACTIVE
                ).count(),
                "applications": AdoptionApplication.objects.count(),
            },
            "featured_animal": Animal.objects.filter(
                is_published=True,
                adoption_status=Animal.AdoptionStatus.AVAILABLE,
            )
            .select_related("category", "campus")
            .prefetch_related("images", "tags")
            .first(),
            "campus_snapshots": Campus.objects.filter(is_active=True)
            .annotate(
                available_animals=Count(
                    "animals",
                    filter=Q(
                        animals__is_published=True,
                        animals__adoption_status=Animal.AdoptionStatus.AVAILABLE,
                    ),
                )
            )
            .order_by("-available_animals", "name")[:3],
            "faqs": faqs_for(FAQModule.ADOPTION),
        },
    )


def adoption_detail(request: HttpRequest, pk: int) -> HttpResponse:
    animal = get_object_or_404(
        Animal.objects.select_related("category", "campus").prefetch_related(
            "images", "tags"
        ),
        pk=pk,
        is_published=True,
        adoption_status__in=(
            Animal.AdoptionStatus.AVAILABLE,
            Animal.AdoptionStatus.ADOPTED,
        ),
    )
    return render(
        request,
        "adoptions/detail.html",
        {"animal": animal, "form": AdoptionApplicationForm()},
    )


@require_POST
@login_required
def apply(request: HttpRequest, pk: int) -> HttpResponse:
    animal = get_object_or_404(Animal, pk=pk, is_published=True)
    form = AdoptionApplicationForm(request.POST)
    if form.is_valid():
        try:
            submit_adoption_application(
                applicant=request.user, animal_id=animal.pk, **form.cleaned_data
            )
        except AdoptionError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "领养申请已提交，请等待审核。")
            return redirect("adoptions:mine")
    return render(
        request, "adoptions/detail.html", {"animal": animal, "form": form}, status=400
    )


@login_required
def mine(request: HttpRequest) -> HttpResponse:
    user = cast(Any, request.user)
    applications = AdoptionApplication.objects.filter(applicant=user).select_related(
        "animal", "animal__category"
    )
    relationships = AdoptionRelationship.objects.filter(adopter=user).select_related(
        "animal", "animal__category"
    )
    return render(
        request,
        "adoptions/mine.html",
        {"applications": applications, "relationships": relationships},
    )
