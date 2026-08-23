from django.urls import path

from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .consts import APP_NAME

app_name = APP_NAME

# Rutas comentadas para referencia futura
# path('', views.ViewPurchase.as_view(), name='index'),
# path('profile/', views.ProfileView.as_view(), name='profile'),
# path("detail/<int:pk>", views.DetailView.as_view(), name="detail"),

urlpatterns = generate_crud_urls(views)

urlpatterns += [
    path("grupos/<int:pk>/", views.AddGroupView.as_view(), name="groups"),
    path("ban/<int:pk>/", views.BanUserView.as_view(), name="ban"),
    path(
        "fields/user/auto.json",
        views.UserSelect2ResponseView.as_view(),
        name="user_select2",
    ),
]
