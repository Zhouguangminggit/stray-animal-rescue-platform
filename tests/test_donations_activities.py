from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from apps.activities.models import Activity, Participation
from apps.activities.services import (
    ActivityError,
    cancel_participation,
    register_activity,
)
from apps.campuses.models import Campus, School
from apps.donations.models import DonationItem, DonationProject, Pledge
from apps.donations.services import DonationError, create_pledge, update_pledge_status


@pytest.fixture
def participation_context(db):
    user = get_user_model().objects.create_user(
        username="participant", email="participant@example.com", password="pass12345"
    )
    school = School.objects.create(name="测试大学")
    campus = Campus.objects.create(school=school, name="主校区")
    now = timezone.now()
    return user, campus, now


@pytest.mark.django_db
def test_pledge_cannot_exceed_remaining_quantity(participation_context) -> None:
    user, _, now = participation_context
    project = DonationProject.objects.create(
        title="猫粮计划",
        summary="急需猫粮",
        description="说明",
        status=DonationProject.Status.OPEN,
        starts_at=now - timedelta(days=1),
        ends_at=now + timedelta(days=1),
    )
    item = DonationItem.objects.create(
        project=project, name="猫粮", unit="袋", required_quantity=5
    )
    pledge = create_pledge(user=user, item_id=item.pk, quantity=4)
    with pytest.raises(DonationError):
        create_pledge(user=user, item_id=item.pk, quantity=2)
    update_pledge_status(pledge_id=pledge.pk, status=Pledge.Status.CANCELLED)
    assert create_pledge(user=user, item_id=item.pk, quantity=5).quantity == 5


@pytest.mark.django_db
def test_donation_list_shows_summary_modules(client, participation_context) -> None:
    _, _, now = participation_context
    project = DonationProject.objects.create(
        title="猫粮计划",
        summary="急需猫粮",
        description="说明",
        status=DonationProject.Status.OPEN,
        starts_at=now - timedelta(days=1),
        ends_at=now + timedelta(days=1),
    )
    DonationItem.objects.create(
        project=project, name="猫粮", unit="袋", required_quantity=5
    )

    response = client.get(reverse("donations:list"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "捐赠数据概览" in content
    assert "急需物资" in content


@pytest.mark.django_db
def test_activity_capacity_and_cancel_release_place(participation_context) -> None:
    user, campus, now = participation_context
    other = get_user_model().objects.create_user(
        username="other", email="other@example.com", password="pass12345"
    )
    activity = Activity.objects.create(
        title="救助宣传",
        summary="摘要",
        content="内容",
        campus=campus,
        location="广场",
        starts_at=now + timedelta(days=2),
        ends_at=now + timedelta(days=2, hours=2),
        registration_starts_at=now - timedelta(days=1),
        registration_ends_at=now + timedelta(days=1),
        capacity=1,
        status=Activity.Status.OPEN,
    )
    participation = register_activity(user=user, activity_id=activity.pk)
    with pytest.raises(ActivityError):
        register_activity(user=other, activity_id=activity.pk)
    cancel_participation(participation_id=participation.pk, user=user)
    assert (
        register_activity(user=other, activity_id=activity.pk).status
        == Participation.Status.REGISTERED
    )


@pytest.mark.django_db
def test_activity_list_shows_summary_modules(client, participation_context) -> None:
    _, campus, now = participation_context
    Activity.objects.create(
        title="救助宣传",
        summary="摘要",
        content="内容",
        campus=campus,
        location="广场",
        starts_at=now + timedelta(days=2),
        ends_at=now + timedelta(days=2, hours=2),
        registration_starts_at=now - timedelta(days=1),
        registration_ends_at=now + timedelta(days=1),
        capacity=12,
        status=Activity.Status.OPEN,
    )

    response = client.get(reverse("activities:list"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "活动数据概览" in content
    assert "校区活动概览" in content
