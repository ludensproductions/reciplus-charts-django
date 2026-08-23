from django.urls import path

from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .consts import APP_NAME

app_name = APP_NAME

urlpatterns = generate_crud_urls(views)

urlpatterns += [
    path("disabled-index/", views.DisabledIndexView.as_view(), name="disabled_index"),
    path("enable/<int:pk>", views.EnableView.as_view(), name="enable"),
    path("grupos/<int:pk>/", views.AddGroupView.as_view(), name="groups"),
    path(
        "fields/position/auto.json",
        views.PositionSelect2responseView.as_view(),
        name="position_select2",
    ),
]
