from django.urls import path

from . import views

app_name = "adoptions"
urlpatterns = [
    path("", views.adoption_list, name="list"),
    path("mine/", views.mine, name="mine"),
    path("<int:pk>/", views.adoption_detail, name="detail"),
    path("<int:pk>/apply/", views.apply, name="apply"),
]
