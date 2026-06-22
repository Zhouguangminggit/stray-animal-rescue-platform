from django.urls import path

from . import views

app_name = "animals"
urlpatterns = [
    path("", views.animal_list, name="list"),
    path("<int:pk>/", views.animal_detail, name="detail"),
    path("rescue/create/", views.rescue_create, name="rescue_create"),
    path("rescue/mine/", views.my_rescues, name="my_rescues"),
]
