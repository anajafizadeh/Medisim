from rest_framework.permissions import BasePermission

class IsInstructor(BasePermission):
    """
    Allows access only to instructors (or staff/superusers).
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "role", "student") == "instructor" or user.is_staff or user.is_superuser