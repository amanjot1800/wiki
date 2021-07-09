from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("q", views.q, name="q"),
    path("random", views.random, name="random"),
    path("<str:title2>/edit/", views.edit, name="edit"),
    path("<str:title>", views.fetch, name="fetch"),
]
