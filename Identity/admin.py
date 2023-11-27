from django.contrib import admin
from . import models
from typing import Any
from django.db.models.query import QuerySet
from django.http.request import HttpRequest


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender',
                    'mobile', 'is_student', 'is_teacher', 'is_chancellor', 'is_it_manager')
    list_filter = ('username', 'email', 'first_name', 'last_name', 'gender',
                   'mobile', 'is_student', 'is_teacher', 'is_chancellor', 'is_it_manager')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'gender',
                     'mobile', 'is_student', 'is_teacher', 'is_chancellor', 'is_it_manager')


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry_year', 'entry_term',
                    'current_term', 'average', 'academic_year')
    list_filter = ('user', 'entry_year', 'entry_term',
                   'current_term', 'average', 'academic_year')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email',
                     'user__ national_code', 'entry_year', 'entry_term', 'current_term', 'average', 'academic_year')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        user = request.user
        chancellor_college = user.college
        if user.is_chancellor:
            qs = qs.filter(college=chancellor_college)
        return qs


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'expert')
    list_filter = ('user', 'level', 'expert')
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'user__email', 'user__ national_code', 'level', 'expert')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        user = request.user
        chancellor_college = user.college
        if user.is_chancellor:
            qs = qs.filter(college=chancellor_college)
        return qs
