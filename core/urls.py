from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("fleet/", views.fleet_list, name="fleet_list"),
    path("destinations/", views.destination_list, name="destination_list"),
    path("destinations/<slug:slug>/", views.destination_detail, name="destination_detail"),
    path("our-story/", views.story, name="story"),
    path("contact/", views.contact, name="contact"),
]
