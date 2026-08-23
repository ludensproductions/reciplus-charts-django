from django.urls import path

from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .consts import APP_NAME

app_name = APP_NAME

urlpatterns = generate_crud_urls(views)

urlpatterns += [
    path("attendees/<int:pk>/", views.AddEventAttendeeView.as_view(), name="event-attendees"),
    path("download_map/", views.DownloadStaticPDFView.as_view(), name="download-map"),
    path("clone_event/<int:pk>/", views.CloneEventView.as_view(), name="clone-event"),
]
