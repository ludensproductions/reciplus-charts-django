from django.urls import path

from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .consts import APP_NAME

app_name = APP_NAME

urlpatterns = generate_crud_urls(views, include=["index", "edit"])


urlpatterns += [
    path("asignar-grupos/<int:pk>", views.AsignarGruposView.as_view(), name="permissions"),
]
