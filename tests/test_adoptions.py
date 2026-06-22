import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from apps.adoptions.models import AdoptionApplication, AdoptionRelationship
from apps.adoptions.services import (
    AdoptionLimitReached,
    InvalidAdoptionState,
    end_adoption_relationship,
    review_adoption_application,
    submit_adoption_application,
)
from apps.animals.models import Animal, AnimalCategory, ReviewStatus
from apps.campuses.models import Campus, School
from apps.notifications.models import Notification

PASSWORD = "Harness-test-password-2026"


@pytest.fixture
def adoption_context(db):
    school = School.objects.create(name="测试大学")
    campus = Campus.objects.create(school=school, name="主校区")
    category = AnimalCategory.objects.create(name="猫")
    user_model = get_user_model()
    applicant = user_model.objects.create_user(
        username="adopter", email="adopter@example.com", password=PASSWORD
    )
    other = user_model.objects.create_user(
        username="other", email="other@example.com", password=PASSWORD
    )
    reviewer = user_model.objects.create_superuser(
        username="reviewer", email="reviewer@example.com", password=PASSWORD
    )
    animal = Animal.objects.create(
        category=category,
        name="小橘",
        campus=campus,
        found_location="图书馆",
        description="性格温顺",
        rescue_status=Animal.RescueStatus.RESCUED,
        adoption_status=Animal.AdoptionStatus.AVAILABLE,
        is_published=True,
        published_at=timezone.now(),
    )
    return campus, category, applicant, other, reviewer, animal


def application_payload() -> dict[str, str]:
    return {
        "motivation": "希望给它稳定的家",
        "housing": "校外整租",
        "experience": "有养猫经验",
        "contact": "13800138000",
    }


@pytest.mark.django_db
def test_adoption_application_requires_login_and_prevents_duplicate(
    client, adoption_context
) -> None:
    _, _, applicant, _, _, animal = adoption_context
    assert (
        client.post(
            reverse("adoptions:apply", args=(animal.pk,)), application_payload()
        ).status_code
        == 302
    )
    client.force_login(applicant)
    response = client.post(
        reverse("adoptions:apply", args=(animal.pk,)), application_payload()
    )
    assert response.status_code == 302
    assert AdoptionApplication.objects.count() == 1
    duplicate = client.post(
        reverse("adoptions:apply", args=(animal.pk,)), application_payload()
    )
    assert duplicate.status_code == 400
    assert AdoptionApplication.objects.count() == 1


@pytest.mark.django_db
def test_approval_creates_relationship_and_rejects_competitors(
    adoption_context,
) -> None:
    _, _, applicant, other, reviewer, animal = adoption_context
    application = submit_adoption_application(
        applicant=applicant, animal_id=animal.pk, **application_payload()
    )
    competitor = submit_adoption_application(
        applicant=other, animal_id=animal.pk, **application_payload()
    )

    result = review_adoption_application(
        application_id=application.pk,
        reviewer=reviewer,
        decision=ReviewStatus.APPROVED,
        note="条件符合",
    )

    animal.refresh_from_db()
    competitor.refresh_from_db()
    assert result.relationship is not None
    assert animal.adoption_status == Animal.AdoptionStatus.ADOPTED
    assert competitor.status == ReviewStatus.REJECTED
    assert (
        Notification.objects.filter(
            business_type=Notification.BusinessType.ADOPTION
        ).count()
        == 2
    )
    with pytest.raises(InvalidAdoptionState):
        review_adoption_application(
            application_id=application.pk,
            reviewer=reviewer,
            decision=ReviewStatus.APPROVED,
        )


@pytest.mark.django_db
def test_active_adoption_limit_is_three(adoption_context) -> None:
    campus, category, applicant, _, _, animal = adoption_context
    for index in range(3):
        adopted_animal = Animal.objects.create(
            category=category,
            name=f"已领养{index}",
            campus=campus,
            found_location="校内",
            description="测试",
            adoption_status=Animal.AdoptionStatus.ADOPTED,
        )
        application = AdoptionApplication.objects.create(
            applicant=applicant,
            animal=adopted_animal,
            motivation="测试",
            housing="测试",
            contact="13800138000",
            status=ReviewStatus.APPROVED,
        )
        AdoptionRelationship.objects.create(
            application=application,
            adopter=applicant,
            animal=adopted_animal,
            started_at=timezone.now(),
        )

    with pytest.raises(AdoptionLimitReached):
        submit_adoption_application(
            applicant=applicant, animal_id=animal.pk, **application_payload()
        )


@pytest.mark.django_db
def test_ending_relationship_releases_animal(adoption_context) -> None:
    _, _, applicant, _, reviewer, animal = adoption_context
    application = submit_adoption_application(
        applicant=applicant, animal_id=animal.pk, **application_payload()
    )
    relationship = review_adoption_application(
        application_id=application.pk, reviewer=reviewer, decision=ReviewStatus.APPROVED
    ).relationship
    assert relationship is not None

    end_adoption_relationship(relationship_id=relationship.pk, note="双方协商终止")

    relationship.refresh_from_db()
    animal.refresh_from_db()
    assert relationship.status == AdoptionRelationship.Status.ENDED
    assert animal.adoption_status == Animal.AdoptionStatus.AVAILABLE
