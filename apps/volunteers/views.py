from typing import Any, cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.animals.models import ReviewStatus
from apps.faqs.models import FAQModule, faqs_for

from .forms import CommunityPostForm, CommunityReportForm, VolunteerApplicationForm
from .models import (
    CommunityArticle,
    CommunityPost,
    CommunityReport,
    VolunteerApplication,
    VolunteerProfile,
)


def community_list(request: HttpRequest) -> HttpResponse:
    articles = CommunityArticle.objects.filter(
        is_published=True, published_at__isnull=False
    ).prefetch_related("tags")[:6]
    posts = Paginator(
        CommunityPost.objects.filter(is_hidden=False).select_related("author"), 12
    ).get_page(request.GET.get("page"))
    return render(
        request,
        "volunteers/community_list.html",
        {
            "articles": articles,
            "page_obj": posts,
            "faqs": faqs_for(FAQModule.VOLUNTEER),
        },
    )


def article_detail(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(
        CommunityArticle.objects.prefetch_related("tags"),
        pk=pk,
        is_published=True,
        published_at__isnull=False,
    )
    return render(request, "volunteers/article_detail.html", {"article": article})


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(
        CommunityPost.objects.select_related("author"), pk=pk, is_hidden=False
    )
    return render(
        request,
        "volunteers/post_detail.html",
        {"post": post, "report_form": CommunityReportForm()},
    )


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = CommunityPostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "帖子已发布。")
        return redirect("volunteers:post_detail", pk=post.pk)
    return render(
        request,
        "volunteers/form.html",
        {"form": form, "title": "发布社区帖子", "submit_label": "发布"},
    )


@require_POST
@login_required
def report_post(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(CommunityPost, pk=pk, is_hidden=False)
    form = CommunityReportForm(request.POST)
    if form.is_valid():
        try:
            CommunityReport.objects.create(
                reporter=cast(Any, request.user),
                post=post,
                reason=form.cleaned_data["reason"],
            )
        except IntegrityError:
            messages.error(request, "您已举报过该帖子，请等待处理。")
        else:
            messages.success(request, "举报已提交。")
    return redirect("volunteers:post_detail", pk=post.pk)


@login_required
def volunteer_apply(request: HttpRequest) -> HttpResponse:
    user = cast(Any, request.user)
    if VolunteerApplication.objects.filter(
        applicant=user, status=ReviewStatus.PENDING
    ).exists():
        messages.info(request, "您已有待审核的志愿者申请。")
        return redirect("volunteers:mine")
    form = VolunteerApplicationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.applicant = user
        application.save()
        messages.success(request, "志愿者申请已提交。")
        return redirect("volunteers:mine")
    return render(
        request,
        "volunteers/form.html",
        {
            "form": form,
            "title": "加入志愿者",
            "submit_label": "提交申请",
            "multipart": True,
        },
    )


@login_required
def mine(request: HttpRequest) -> HttpResponse:
    user = cast(Any, request.user)
    return render(
        request,
        "volunteers/mine.html",
        {
            "applications": VolunteerApplication.objects.filter(applicant=user),
            "profile": VolunteerProfile.objects.filter(user=user).first(),
            "posts": CommunityPost.objects.filter(author=user),
        },
    )
