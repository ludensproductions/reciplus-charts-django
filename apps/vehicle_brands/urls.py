from django.urls import path

from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .const import APP_NAME

app_name = APP_NAME

urlpatterns = generate_crud_urls(views, include=["index", "create", "edit", "delete", "detail"])
