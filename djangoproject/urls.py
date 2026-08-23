"""djangoproject URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

import django_eventstream
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path

from apps.users import views as users_views

from .api import api

ENABLE_OAUTH2_LOGIN = settings.ENABLE_OAUTH2_LOGIN

urlpatterns = (
    [
        path("select2/", include("apps.select2.urls")),
        path("events/<channel>/", include(django_eventstream.urls)),
        path("admin/", admin.site.urls),
        path("albums/", include("apps.albums.urls")),
        path("categories/", include("apps.categories.urls")),
        path("contents/", include("apps.contents.urls")),
        path("articles/", include("apps.articles.urls")),
        path("videos/", include("apps.videos.urls")),
        path("dashboard/", include("apps.dashboard.urls")),
        path("evidence/", include("apps.evidence.urls")),
        path("sales/", include("apps.sales.urls")),
        path("facturas/", include("apps.facturas.urls")),
        path("movies/", include("apps.movies.urls")),
        path("genres/", include("apps.genres.urls")),
        path("jobs/", include("apps.jobs.urls")),
        path("movies-inventory/", include("apps.movie_inventory.urls")),
        path("groups/", include("apps.groups.urls")),
        path("log/", include("apps.history.urls")),
        path("oauth2/", include("apps.oauth2.urls"), name="oauth2"),
        path("music-tags/", include("apps.music_tags.urls")),
        path("music-genres/", include("apps.music_genres.urls")),
        path("music-themes/", include("apps.music_themes.urls")),
        path("song-reviews/", include("apps.song_reviews.urls")),
        path("reservations/", include("apps.reservations.urls")),
        path("departments/", include("apps.departments.urls")),
        path("tipo-productos/", include("apps.tipo_productos.urls")),
        path("productos/", include("apps.productos.urls")),
        path("positions/", include("apps.positions.urls")),
        path("abarrotes/", include("apps.abarrotes.urls")),
        path("bodega/", include("apps.bodega.urls")),
        path("activities/", include("apps.activities.urls")),
        path("activity-feed/", include("apps.activity_feed.urls")),
        path("chat/", include("apps.chat.urls")),
        path("event-planner/", include("apps.event_planner.urls")),
        path("students/", include("apps.students.urls")),
        path(
            "vehicles/",
            include("apps.vehicles.urls"),
        ),
        path("vehicle-types/", include("apps.vehicle_types.urls")),
        path("vehicle-brands/", include("apps.vehicle_brands.urls")),
        path("simple-report/", include("apps.simple_report.urls")),
        path("catalogos/", include("apps.catalogos.urls")),
        path("usuarios/", include("apps.users_module.urls")),
        # Microsoft OAuth2
        path("", include("apps.microsoft.urls")),
        # Discord OAuth2
        path("", include("apps.discord.urls")),
        # User and Registration urls
        path(
            "",
            users_views.LoginView.as_view(redirect_authenticated_user=True)
            if ENABLE_OAUTH2_LOGIN
            else users_views.NormalLoginView.as_view(redirect_authenticated_user=True),
            name="login",
        ),
        path("profile/", users_views.ProfileView.as_view(), name="profile"),
        path(
            "logout/",
            users_views.LogoutRedirectView.as_view()
            if ENABLE_OAUTH2_LOGIN
            else users_views.NormalLogoutView.as_view(),
            name="logout",
        ),
        path("register/", users_views.RegisterView.as_view(), name="register"),
        path(
            "register-admin/",
            staff_member_required(users_views.RegisterViewAdmin.as_view()),
            name="registerAdmin",
        ),
        path("forgot-password/", users_views.ForgotPasswordView.as_view(), name="forgot-password"),
        path(
            "password-reset-done/",
            users_views.PasswordResetDoneView.as_view(),
            name="password_reset_done",
        ),
        path(
            "password-reset/<uidb64>/<token>/",
            users_views.CustomPasswordResetConfirmView.as_view(),
            name="password_reset_confirm",
        ),
        path(
            "password-reset-complete/",
            users_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete",
        ),
        path("users/", include("apps.users.urls")),
        path("api/", api.urls),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEVELOPMENT:
    from debug_toolbar.toolbar import debug_toolbar_urls  # This is here due to development variable

    urlpatterns += debug_toolbar_urls()

# Remember that the last line regarding file/image uploads must be changed for production purposes:
# https://docs.djangoproject.com/en/4.0/howto/static-files/deployment/
