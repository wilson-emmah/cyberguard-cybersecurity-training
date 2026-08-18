from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    message = "Administrator access required."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_staff or user.is_superuser:
            return True

        try:
            return user.profile.role == "admin"
        except Exception:
            return False
