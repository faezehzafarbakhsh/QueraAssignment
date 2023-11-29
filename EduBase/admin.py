from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
# Register your models here.

# EduField


@admin.register(models.EduField)
class EduFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'edu_group', 'unit_count', 'edu_grade')
    list_filter = ('name', 'edu_group', 'unit_count', 'edu_grade')
    search_fields = ('name', 'edu_group', 'unit_count', 'edu_grade')


# Course


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'college', 'unit_count', 'course_type')
    list_filter = ('name', 'college', 'unit_count', 'course_type')
    search_fields = ('name', 'college', 'unit_count', 'course_type')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        user = request.user
        chancellor_college = user.college
        if user.is_chancellor:
            qs = qs.filter(college=chancellor_college)
        return qs


# CourseRelation

@admin.register(models.CourseRelation)
class CourseRelationAdmin(admin.ModelAdmin):
    list_display = ('primary_course', 'secondary_course', 'relation_type')
    list_filter = ('primary_course', 'secondary_course', 'relation_type')
    search_fields = ('primary_course', 'secondary_course', 'relation_type')


# College
@admin.register(models.College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
