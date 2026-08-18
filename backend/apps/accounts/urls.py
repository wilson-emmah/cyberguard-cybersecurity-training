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
    # User registration
    path(
        'auth/register/',
        RegisterView.as_view(),
        name='register'
    ),

    # Login - returns access and refresh JWT tokens
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    # Refresh access token
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # Currently authenticated user
    path(
        'auth/me/',
        MeView.as_view(),
        name='me'
    ),

    # Admin endpoints
    path(
        'admin/users/',
        AdminUsersView.as_view(),
        name='admin-users'
    ),

    path(
        'admin/stats/',
        AdminStatsView.as_view(),
        name='admin-stats'
    ),
]
