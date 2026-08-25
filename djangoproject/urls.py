"""djangoproject URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .api import api

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", api.urls),
        path("graphs/", include("apps.graphs.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEVELOPMENT:
    from debug_toolbar.toolbar import debug_toolbar_urls  # This is here due to development variable

    urlpatterns += debug_toolbar_urls()

# Remember that the last line regarding file/image uploads must be changed for production purposes:
# https://docs.djangoproject.com/en/4.0/howto/static-files/deployment/
