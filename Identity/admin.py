from django.contrib import admin
from .models import User, Student, Teacher
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'mobile', 'is_student', 'is_teacher', 'is_chancellor', 'is_it_manager')
    list_filter = ('username', 'email', 'first_name', 'last_name', 'gender', 'mobile', 'is_student', 'is_teacher', 'is_chancellor', 'is_it_manager')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'mobile', 'is_student', 'is_teacher', 'is_chancellor', 'is_it_manager')


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry_year', 'entry_term', 'current_term', 'average', 'academic_year')
    list_filter = ('user', 'entry_year', 'entry_term', 'current_term', 'average', 'academic_year')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'user__ national_code', 'entry_year', 'entry_term', 'current_term', 'average', 'academic_year')


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'expert')
    list_filter = ('user', 'level', 'expert')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'user__ national_code', 'level', 'expert')