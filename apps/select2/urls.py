from django.urls import path

from .views import CustomAutoResponseView

app_name = "django_select2"

urlpatterns = [
    path("fields/auto.json", CustomAutoResponseView.as_view(), name="auto-json"),
]
