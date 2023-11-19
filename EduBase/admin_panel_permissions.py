from rest_framework.permissions import BasePermission


class BaseChancellorPermission(BasePermission):
    """
    Custom permission to check if the user is a Chancellor.
    """

    def has_permission(self, request, view=None):
        return request.user.is_authenticated and request.user.is_chancellor

    def has_add_permission(self, request, view=None):
        return True

    def has_view_permission(self, request, view=None):
        return True


class AdminPanelChancellorPermission(BaseChancellorPermission):

    def has_add_permission(self, request, view=None):
        if not super().has_permission(request, view):
            return False

        college = request.POST.get('college')
        if college is None:
            return False

        return request.user.college == college

    def has_view_permission(self, request, view=None):
        if not super().has_permission(request, view):
            return False
        return True
