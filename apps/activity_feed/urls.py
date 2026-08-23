from apps.comun.common_modules_urls import generate_crud_urls

from . import views

app_name = "activity_feed"

urlpatterns = generate_crud_urls(views)
