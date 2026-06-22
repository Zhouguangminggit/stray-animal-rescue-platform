from typing import Any, cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from apps.campuses.models import Campus
from apps.faqs.models import FAQModule, faqs_for

from .forms import RescueRequestForm
from .models import Animal, AnimalCategory, RescueRequest, RescueRequestImage


def animal_list(request: HttpRequest) -> HttpResponse:
    animals = (
        Animal.objects.filter(is_published=True)
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
        animals = animals.filter(rescue_status=status)
    page = Paginator(animals, 12).get_page(request.GET.get("page"))
    return render(
        request,
        "animals/list.html",
        {
            "page_obj": page,
            "categories": AnimalCategory.objects.filter(is_active=True),
            "campuses": Campus.objects.filter(is_active=True),
            "health_choices": Animal._meta.get_field("health_status").choices,
            "status_choices": Animal.RescueStatus.choices,
            "faqs": faqs_for(FAQModule.RESCUE),
        },
    )


def animal_detail(request: HttpRequest, pk: int) -> HttpResponse:
    animal = get_object_or_404(
        Animal.objects.select_related("category", "campus").prefetch_related(
            "images", "tags"
        ),
        pk=pk,
        is_published=True,
    )
    return render(request, "animals/detail.html", {"animal": animal})


@login_required
@require_http_methods(["GET", "POST"])
def rescue_create(request: HttpRequest) -> HttpResponse:
    form = RescueRequestForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            rescue_request = form.save(commit=False)
            rescue_request.applicant = request.user
            rescue_request.save()
            RescueRequestImage.objects.bulk_create(
                [
                    RescueRequestImage(
                        rescue_request=rescue_request, image=image, sort_order=index
                    )
                    for index, image in enumerate(form.cleaned_data["images"])
                ]
            )
        messages.success(request, "救助申请已提交，请等待审核。")
        return redirect("animals:my_rescues")
    return render(request, "animals/rescue_form.html", {"form": form})


@login_required
def my_rescues(request: HttpRequest) -> HttpResponse:
    page = Paginator(
        RescueRequest.objects.filter(applicant=cast(Any, request.user)).select_related(
            "category", "campus", "approved_animal"
        ),
        10,
    ).get_page(request.GET.get("page"))
    return render(request, "animals/my_rescues.html", {"page_obj": page})
