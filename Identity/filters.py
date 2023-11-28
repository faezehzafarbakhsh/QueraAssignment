from django_filters import rest_framework as filters
from Identity import models


class TeacherFilter(filters.FilterSet):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'teachers__level', 'teachers__expert']

class StudentFilter(filters.FilterSet):
    class Meta:
        model = models.Teacher
        fields = ['user__first_name', 'user__last_name', 'user__username' ]