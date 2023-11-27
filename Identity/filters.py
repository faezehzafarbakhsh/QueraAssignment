from django_filters import rest_framework as filters
from Identity import models


class StudentFilter(filters.FilterSet):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username' ]