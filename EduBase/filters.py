from django_filters import rest_framework as filters
from EduBase import models
from EduTerm import models as edeutermmodel

class ListCourseFilter(filters.FilterSet):
    class Meta:
        model = models.Course
        fields = ['college', 'name']


class ListCourseTermFilter(filters.FilterSet):
    class Meta:
        model = edeutermmodel.CourseTerm
        fields = ['course__college', 'course__name', 'term__name']