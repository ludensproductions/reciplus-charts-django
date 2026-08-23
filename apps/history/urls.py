from django.urls import path

from . import views

app_name = "history"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("users/", views.UserLogsView.as_view(), name="users"),
    path(
        "recover-users/<int:pk>/",
        views.UserRollbackView.as_view(),
        name="recover-users",
    ),
    path("generic-log/", views.GenericIndexview.as_view(), name="generic-log"),
    path(
        "history/<str:model>/<str:app>",
        views.GenericLogsView.as_view(),
        name="generic-log-model",
    ),
    path(
        "history/<str:model>/<str:app>/<int:pk>",
        views.DetailView.as_view(),
        name="generic-detail",
    ),
    path(
        "recover-users/<str:model>/<str:app>/<int:pk>",
        views.GenericRollbackView.as_view(),
        name="generic-recover",
    ),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
]
