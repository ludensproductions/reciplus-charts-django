from django.urls import path

from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .consts import APP_NAME

app_name = APP_NAME

urlpatterns = generate_crud_urls(views)

urlpatterns += [
    path("enable/<int:pk>", views.EnableView.as_view(), name="enable"),
    path("disabled-index/", views.DisabledIndexView.as_view(), name="disabled_index"),
]
