from django.urls import path

from . import views

app_name = "oauth2"

urlpatterns = [
    path("authorize/", views.OAuthAuthorizeView.as_view(), name="authorize"),
    path("callback/", views.OAuthCallbackView.as_view(), name="callback"),
    path("logout/", views.OAuthLogoutView.as_view(), name="logout"),
    path("successful-logout/", views.SuccessfulLogoutView.as_view(), name="successful_logout"),
]
