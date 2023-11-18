from rest_framework.permissions import BasePermission


class BaseChancellorPermission(BasePermission):
    """
    Custom permission to check if the user is a Chancellor.
    """

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.is_chancellor


class AdminPanelChancellorPermission(BaseChancellorPermission):
    def has_add_permission(self, request):
        if not super().has_permission(request):
            return False

        college = request.POST.get('college')
        if college is None:
            return False

        return request.user.college == college
