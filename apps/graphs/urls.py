from django.urls import path

from apps.graphs import views

app_name = "graphs"

urlpatterns = [
    path("", views.index, name="index"),
]
