from apps.comun.common_modules_urls import generate_crud_urls

from . import views

app_name = "chat"

urlpatterns = generate_crud_urls(views)
