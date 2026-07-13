from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("fleet/", views.fleet_list, name="fleet_list"),
    path("destinations/", views.destination_list, name="destination_list"),
    path("destinations/<slug:slug>/", views.destination_detail, name="destination_detail"),
    path("our-story/", views.story, name="story"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),
]
