import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from apps.animals.models import (
    Animal,
    AnimalCategory,
    HealthStatus,
    RescueRequest,
    ReviewStatus,
)
from apps.animals.services import InvalidReviewState, review_rescue_request
from apps.campuses.models import Campus, School
from apps.notifications.models import Notification

PASSWORD = "Harness-test-password-2026"


@pytest.fixture
def animal_context(db):
    school = School.objects.create(name="测试大学")
    campus = Campus.objects.create(school=school, name="主校区")
    category = AnimalCategory.objects.create(name="猫")
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username="rescuer", email="rescuer@example.com", password=PASSWORD
    )
    reviewer = user_model.objects.create_superuser(
        username="reviewer", email="reviewer@example.com", password=PASSWORD
    )
    return campus, category, user, reviewer


@pytest.mark.django_db
def test_public_animal_list_only_shows_published(client, animal_context) -> None:
    campus, category, _, _ = animal_context
    visible = Animal.objects.create(
        category=category,
        name="小橘",
        campus=campus,
        found_location="图书馆",
        description="待救助",
        is_published=True,
        published_at=timezone.now(),
    )
    hidden = Animal.objects.create(
        category=category,
        name="隐藏动物",
        campus=campus,
        found_location="未知",
        description="不公开",
        is_published=False,
    )

    response = client.get(reverse("animals:list"))

    assert response.status_code == 200
    content = response.content.decode()
    assert visible.name in content
    assert hidden.name not in content
    assert "救助数据概览" in content
    assert "救助流程" in content
    assert client.get(reverse("animals:detail", args=(hidden.pk,))).status_code == 404


@pytest.mark.django_db
def test_rescue_submission_requires_login_and_is_owned(client, animal_context) -> None:
    campus, category, user, _ = animal_context
    assert client.get(reverse("animals:rescue_create")).status_code == 302
    client.force_login(user)

    response = client.post(
        reverse("animals:rescue_create"),
        {
            "category": category.pk,
            "animal_name": "小白",
            "gender": "unknown",
            "health_status": HealthStatus.INJURED,
            "campus": campus.pk,
            "found_location": "南门",
            "description": "腿部受伤",
            "contact": "13800138000",
        },
    )

    assert response.status_code == 302
    rescue_request = RescueRequest.objects.get()
    assert rescue_request.applicant == user
    assert rescue_request.status == ReviewStatus.PENDING


@pytest.mark.django_db
def test_approve_rescue_creates_animal_and_notification(animal_context) -> None:
    campus, category, user, reviewer = animal_context
    rescue_request = RescueRequest.objects.create(
        applicant=user,
        category=category,
        animal_name="小黑",
        health_status=HealthStatus.SICK,
        campus=campus,
        found_location="宿舍楼下",
        description="需要就医",
        contact="13800138000",
    )

    result = review_rescue_request(
        request_id=rescue_request.pk,
        reviewer=reviewer,
        decision=ReviewStatus.APPROVED,
        note="信息完整",
    )

    rescue_request.refresh_from_db()
    assert result.animal is not None
    assert rescue_request.approved_animal == result.animal
    assert result.animal.is_published is True
    notice = Notification.objects.get(recipient=user)
    assert notice.business_type == Notification.BusinessType.RESCUE
    assert "通过" in notice.content
    with pytest.raises(InvalidReviewState):
        review_rescue_request(
            request_id=rescue_request.pk,
            reviewer=reviewer,
            decision=ReviewStatus.APPROVED,
        )
    assert Animal.objects.count() == 1
    assert Notification.objects.count() == 1


@pytest.mark.django_db
def test_reject_rescue_retains_request_without_animal(animal_context) -> None:
    campus, category, user, reviewer = animal_context
    rescue_request = RescueRequest.objects.create(
        applicant=user,
        category=category,
        campus=campus,
        found_location="校门",
        description="描述",
        contact="13800138000",
    )

    result = review_rescue_request(
        request_id=rescue_request.pk,
        reviewer=reviewer,
        decision=ReviewStatus.REJECTED,
        note="位置信息不足",
    )

    assert result.animal is None
    assert Animal.objects.count() == 0
    assert "驳回" in Notification.objects.get(recipient=user).content
