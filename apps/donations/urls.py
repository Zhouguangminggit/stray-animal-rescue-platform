from django.urls import path

from . import views

app_name = "donations"
urlpatterns = [
    path("", views.project_list, name="list"),
    path("mine/", views.mine, name="mine"),
    path("<int:pk>/", views.project_detail, name="detail"),
    path("items/<int:item_id>/pledge/", views.pledge, name="pledge"),
]
