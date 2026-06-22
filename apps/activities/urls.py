from django.urls import path

from . import views

app_name = "activities"
urlpatterns = [
    path("", views.activity_list, name="list"),
    path("mine/", views.mine, name="mine"),
    path("<int:pk>/", views.activity_detail, name="detail"),
    path("<int:pk>/register/", views.register, name="register"),
    path("participations/<int:pk>/cancel/", views.cancel, name="cancel"),
]
