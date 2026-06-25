import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from apps.animals.models import ReviewStatus
from apps.notifications.models import Notification
from apps.volunteers.models import (
    CommunityArticle,
    CommunityPost,
    CommunityReport,
    VolunteerApplication,
    VolunteerProfile,
)
from apps.volunteers.services import (
    CommunityWorkflowError,
    resolve_community_report,
    review_volunteer_application,
)

PASSWORD = "Harness-test-password-2026"


@pytest.fixture
def community_users(db):
    model = get_user_model()
    applicant = model.objects.create_user(
        username="volunteer", email="volunteer@example.com", password=PASSWORD
    )
    author = model.objects.create_user(
        username="author", email="author@example.com", password=PASSWORD
    )
    reviewer = model.objects.create_superuser(
        username="reviewer", email="reviewer@example.com", password=PASSWORD
    )
    return applicant, author, reviewer


@pytest.mark.django_db
def test_volunteer_approval_creates_profile_and_notification(community_users) -> None:
    applicant, _, reviewer = community_users
    application = VolunteerApplication.objects.create(
        applicant=applicant, intention="参与救助", skills="摄影", availability="周末"
    )

    review_volunteer_application(
        application_id=application.pk,
        reviewer=reviewer,
        decision=ReviewStatus.APPROVED,
        note="审核通过",
    )

    assert VolunteerProfile.objects.filter(
        user=applicant, status=VolunteerProfile.Status.ACTIVE
    ).exists()
    assert Notification.objects.filter(
        recipient=applicant, business_type=Notification.BusinessType.VOLUNTEER
    ).exists()
    with pytest.raises(CommunityWorkflowError):
        review_volunteer_application(
            application_id=application.pk,
            reviewer=reviewer,
            decision=ReviewStatus.APPROVED,
        )


@pytest.mark.django_db
def test_report_hide_flow_hides_post_and_notifies_both_users(community_users) -> None:
    reporter, author, reviewer = community_users
    post = CommunityPost.objects.create(
        author=author, title="不当内容", content="待审核"
    )
    report = CommunityReport.objects.create(
        reporter=reporter, post=post, reason="包含不当信息"
    )

    resolve_community_report(
        report_id=report.pk, reviewer=reviewer, decision="hide", note="举报属实"
    )

    post.refresh_from_db()
    report.refresh_from_db()
    assert post.is_hidden is True
    assert report.status == CommunityReport.Status.RESOLVED
    assert (
        Notification.objects.filter(
            business_type=Notification.BusinessType.REPORT
        ).count()
        == 2
    )


@pytest.mark.django_db
def test_public_community_excludes_hidden_and_unpublished_content(
    client, community_users
) -> None:
    _, author, _ = community_users
    CommunityArticle.objects.create(
        title="公开文章",
        summary="摘要",
        content="内容",
        is_published=True,
        published_at=timezone.now(),
    )
    CommunityArticle.objects.create(
        title="草稿文章", summary="摘要", content="内容", is_published=False
    )
    CommunityPost.objects.create(author=author, title="公开帖子", content="内容")
    CommunityPost.objects.create(
        author=author, title="隐藏帖子", content="内容", is_hidden=True
    )

    content = client.get(reverse("volunteers:community")).content.decode()

    assert "公开文章" in content and "公开帖子" in content
    assert "草稿文章" not in content and "隐藏帖子" not in content
    assert "志愿者社区数据概览" in content
    assert "参与方式" in content


@pytest.mark.django_db
def test_public_community_detail_pages_render(client, community_users) -> None:
    _, author, _ = community_users
    article = CommunityArticle.objects.create(
        title="公开文章",
        summary="摘要",
        content="正文内容",
        is_published=True,
        published_at=timezone.now(),
    )
    post = CommunityPost.objects.create(author=author, title="公开帖子", content="内容")

    article_response = client.get(
        reverse("volunteers:article_detail", args=(article.pk,))
    )
    post_response = client.get(reverse("volunteers:post_detail", args=(post.pk,)))

    assert article_response.status_code == 200
    assert "正文内容" in article_response.content.decode()
    assert post_response.status_code == 200
    assert "公开帖子" in post_response.content.decode()


@pytest.mark.django_db
def test_logged_in_user_can_publish_and_report(client, community_users) -> None:
    reporter, author, _ = community_users
    client.force_login(reporter)
    response = client.post(
        reverse("volunteers:post_create"),
        {"title": "救助分享", "content": "今日救助记录"},
    )
    assert response.status_code == 302
    post = CommunityPost.objects.create(author=author, title="待举报", content="内容")
    response = client.post(
        reverse("volunteers:report_post", args=(post.pk,)), {"reason": "内容有误"}
    )
    assert response.status_code == 302
    assert CommunityReport.objects.filter(reporter=reporter, post=post).exists()
