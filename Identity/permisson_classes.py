from rest_framework.permissions import BasePermission


class IsItManager(BasePermission):
    """
    Custom permission to check if the user is an IT manager.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_it_manager
