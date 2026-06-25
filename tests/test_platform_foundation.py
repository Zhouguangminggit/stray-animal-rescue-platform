import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from apps.campuses.models import Campus, School
from apps.notifications.models import Notification
from apps.tags.models import Tag, TagCategory


@pytest.mark.django_db
def test_single_school_and_campus_membership() -> None:
    school = School.objects.create(name="测试大学")
    campus = Campus.objects.create(school=school, name="主校区")
    user = get_user_model().objects.create_user(
        username="student",
        email="student@example.com",
        password="pass12345",
        campus=campus,
    )
    assert user.campus == campus
    with pytest.raises(ValidationError):
        School.objects.create(name="其他大学")


@pytest.mark.django_db
def test_tag_unique_within_category() -> None:
    category = TagCategory.objects.create(name="性格")
    Tag.objects.create(category=category, name="亲人")
    assert category.tags.count() == 1


@pytest.mark.django_db
def test_notification_is_private_and_marked_read(client) -> None:
    user_model = get_user_model()
    owner = user_model.objects.create_user(
        username="owner", email="owner@example.com", password="pass12345"
    )
    other = user_model.objects.create_user(
        username="other", email="other@example.com", password="pass12345"
    )
    notice = Notification.objects.create(
        recipient=owner, title="审核结果", content="已通过"
    )
    client.force_login(other)
    assert (
        client.get(reverse("notifications:detail", args=(notice.pk,))).status_code
        == 404
    )
    client.force_login(owner)
    assert (
        client.get(reverse("notifications:detail", args=(notice.pk,))).status_code
        == 200
    )
    notice.refresh_from_db()
    assert notice.read_at is not None


@pytest.mark.django_db
def test_site_header_user_dropdown_renders_and_is_not_clipped(client) -> None:
    user = get_user_model().objects.create_user(
        username="admin", email="admin@example.com", password="pass12345"
    )
    client.force_login(user)

    content = client.get(reverse("home")).content.decode()
    assert 'id="user-dropdown"' in content
    assert reverse("notifications:list") in content
    assert "通知" in content

    css = (
        settings.BASE_DIR / "static" / "css" / "components" / "site-shell.css"
    ).read_text()
    header_right_block = css.split(".header-right {", 1)[1].split("}", 1)[0]
    assert "overflow: visible;" in header_right_block
    assert "overflow-x: auto;" not in header_right_block
