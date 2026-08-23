from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .consts import APP_NAME

app_name = APP_NAME

urlpatterns = generate_crud_urls(views)

# Rutas comentadas para referencia futura
# path("deleted/", views.GroupDeletedIndexView.as_view(), name="deleted"),
# path("enable/<int:pk>/", views.GroupEnableView.as_view(), name="enable"),
