from django.urls import path

from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .consts import APP_NAME

app_name = APP_NAME

urlpatterns = generate_crud_urls(views)


urlpatterns += [
    path("export/csv/", views.ExportCSVView.as_view(), name="export_csv"),
    path(
        "fields/song/auto.json",
        views.SongSelect2responseView.as_view(),
        name="song_select2",
    ),
    path(
        "modal-index/",
        views.ModalIndexView.as_view(),
        name="modal_index",
    ),
]
