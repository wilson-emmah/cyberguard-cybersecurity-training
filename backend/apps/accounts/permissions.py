from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    message = "Administrator access required."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff or request.user.is_superuser:
            return True

        try:
            return request.user.profile.role == "admin"
        except Exception:
            return False
