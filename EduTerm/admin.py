from django.contrib import admin
from .models import Term, CourseTerm
from . import models


@admin.register(models.Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'enrollment_start_datetime', 'enrollment_end_datetime', 'class_start_datetime', 'class_end_datetime', 'active_term')
    list_filter = ('name', 'enrollment_start_datetime', 'enrollment_end_datetime', 'class_start_datetime', 'class_end_datetime', 'active_term')
    search_fields = ('name', 'enrollment_start_datetime', 'enrollment_end_datetime', 'class_start_datetime', 'class_end_datetime', 'active_term')


@admin.register(models.CourseTerm)
class CourseTermAdmin(admin.ModelAdmin):
    list_display = ('course', 'term', 'class_day', 'class_time', 'exam_datetime', 'exam_place', 'teacher', 'capacity')
    list_filter = ('course', 'term', 'class_day', 'class_time', 'exam_datetime', 'exam_place', 'teacher', 'capacity')
    search_fields = ('course__name', 'term__name', 'teacher__username', 'class_day', 'class_time', 'exam_datetime', 'exam_place', 'capacity')