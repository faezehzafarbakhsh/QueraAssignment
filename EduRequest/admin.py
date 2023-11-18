from django.contrib import admin
from .models import StudentRequest, EnrollmentCertificate
from . import models


@admin.register(models.StudentRequest)
class StudentRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'course_term', 'status', 'request_type', 'has_academic_year')
    list_filter = ('student', 'term', 'course_term', 'status', 'request_type', 'has_academic_year')
    search_fields = ('student__username', 'term__name', 'course_term__name', 'status', 'request_type', 'has_academic_year')

@admin.register(models.EnrollmentCertificate)
class EnrollmentCertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'enrollment_certificate_place')
    list_filter = ('student', 'term', 'enrollment_certificate_place')
    search_fields = ('student__username', 'term__name', 'enrollment_certificate_place')
