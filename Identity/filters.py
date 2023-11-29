from django_filters import rest_framework as filters
from Identity import models


class TeacherFilter(filters.FilterSet):
    class Meta:
        model = models.User
        fields = ['unique_code', 'first_name', 'last_name',
                  'national_code', 'college', 'teachers__level', 'teachers__expert']


class StudentFilter(filters.FilterSet):
    class Meta:
        model = models.User
        fields = ['unique_code', 'first_name', 'last_name', 'national_code',
                  'college', 'military_service', 'students__entry_year', ]

class ChancellorFilter(filters.FilterSet):
    class Meta:
        model = models.User
        fields = ['unique_code', 'first_name', 'last_name', 'national_code',
                  'college',  ]
