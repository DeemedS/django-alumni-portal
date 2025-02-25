from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):
    """
    Custom permission to allow only staff users to access the API.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
