from django.urls import path

from . import views

app_name = "discord"
urlpatterns = [
    path("login/discord/", views.DiscordLoginView.as_view(), name="login"),
    path("callback/discord/", views.DiscordLoginRedirectView.as_view(), name="redirect"),
]
