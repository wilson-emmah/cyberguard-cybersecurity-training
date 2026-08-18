from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    MeView,
    AdminUsersView,
    AdminStatsView,
)


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),

    path("auth/token/", TokenObtainPairView.as_view(), name="token"),

    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path("auth/me/", MeView.as_view(), name="me"),

    path("admin/users/", AdminUsersView.as_view(), name="admin_users"),

    path("admin/stats/", AdminStatsView.as_view(), name="admin_stats"),
]
