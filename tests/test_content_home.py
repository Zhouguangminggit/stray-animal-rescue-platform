from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone

from apps.animals.models import AnimalCategory
from apps.faqs.models import FAQ, FAQCategory, FAQModule
from apps.posters.models import Poster


@pytest.mark.django_db
def test_poster_validates_link_and_active_window() -> None:
    now = timezone.now()
    invalid = Poster(
        title="非法链接",
        image=SimpleUploadedFile("poster.jpg", b"image"),
        page=Poster.Page.HOME,
        slot=Poster.Slot.BANNER,
        link="javascript:alert(1)",
    )
    with pytest.raises(ValidationError):
        invalid.full_clean()
    active = Poster.objects.create(
        title="公益海报",
        image=SimpleUploadedFile("poster.jpg", b"image"),
        page=Poster.Page.HOME,
        slot=Poster.Slot.BANNER,
        starts_at=now - timedelta(hours=1),
        ends_at=now + timedelta(hours=1),
    )
    Poster.objects.create(
        title="过期海报",
        image=SimpleUploadedFile("old.jpg", b"image"),
        page=Poster.Page.HOME,
        slot=Poster.Slot.BANNER,
        ends_at=now - timedelta(hours=1),
    )
    assert list(Poster.active_for(page=Poster.Page.HOME, slot=Poster.Slot.BANNER)) == [
        active
    ]


@pytest.mark.django_db
def test_rescue_page_displays_module_faq(client) -> None:
    AnimalCategory.objects.create(name="猫")
    category = FAQCategory.objects.create(module=FAQModule.RESCUE, name="救助流程")
    FAQ.objects.create(
        category=category, question="如何发起救助？", answer="登录后填写救助表单。"
    )
    content = client.get(reverse("animals:list")).content.decode()
    assert "如何发起救助？" in content
    assert "登录后填写救助表单" in content


@pytest.mark.django_db
def test_home_uses_business_dashboard_and_empty_states(client) -> None:
    response = client.get(reverse("home"))
    content = response.content.decode()
    assert response.status_code == 200
    assert "让每一个" in content
    assert "最新救助档案" in content
    assert "急需物资" in content
