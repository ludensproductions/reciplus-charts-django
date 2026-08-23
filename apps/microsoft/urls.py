from django.urls import path

from .views import InvalidLoginView, MicrosoftCallbackView, MicrosoftSignInView, MicrosoftSignOutView

app_name = "microsoft"
urlpatterns = [
    path("login/microsoft/", MicrosoftSignInView.as_view(), name="login"),
    path("callback/microsoft/", MicrosoftCallbackView.as_view(), name="redirect"),
    path("logout/microsoft/", MicrosoftSignOutView.as_view(), name="logout"),
    path("login/invalid/", InvalidLoginView.as_view(), name="invalid_login"),
]
