from django.contrib import admin
from . import models
from .models import Enrollment, StudentCourse

# Register your models here.


@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('term', 'student', 'teacher_assistant', 'status', 'taken_term_number')
    list_filter = ('term', 'student', 'teacher_assistant', 'status', 'taken_term_number')
    search_fields = ('student__username', 'teacher_assistant__username', 'term__name', 'status', 'taken_term_number')


@admin.register(models.StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('course_term', 'student', 'status', 'score')
    list_filter = ('course_term', 'student', 'status', 'score')
    search_fields = ('student__username', 'course_term__name', 'status', 'score')
