from rest_framework.permissions import BasePermission


class IsItManager(BasePermission):
    """
    Custom permission to check if the user is an IT manager.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_it_manager


class IsStudent(BasePermission):
    """
    Custom permission to check if the user is an Student.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsTeacher(BasePermission):
    """
    Custom permission to check if the user is an Teacher.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher


class IsChancellor(BasePermission):
    """
    Custom permission to check if the user is a Chancellor.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_chancellor
    
    def has_permission_for_courses(self, request, view, course):
        # Check if the user is a chancellor
        if not request.user.is_authenticated or not request.user.is_chancellor:
            return False

        # Check if the college of the course is equal to the college of the chancellor
        return request.user.college == course.college
        
