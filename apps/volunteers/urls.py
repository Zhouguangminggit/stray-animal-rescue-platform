from django.urls import path

from . import views

app_name = "volunteers"
urlpatterns = [
    path("", views.community_list, name="community"),
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("posts/<int:pk>/report/", views.report_post, name="report_post"),
    path("apply/", views.volunteer_apply, name="apply"),
    path("mine/", views.mine, name="mine"),
]
