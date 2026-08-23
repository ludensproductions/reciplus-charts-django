from .consts import APP_NAME
from . import views
from apps.comun.common_modules_urls import generate_crud_urls

app_name = APP_NAME

urlpatterns = generate_crud_urls(views, include=["index"])