from django.db import models
from django.db.models import Q

import variable_names as vn_edu_request
from django.contrib.auth import get_user_model


# Create your models here.

class StudentRequestManager(models.Manager):
    pass


class StudentRequest(models.Model):
    class StatusChoices(models.IntegerChoices):
        ACCEPT = vn_edu_request.ACCEPT
        DENIED =  vn_edu_request.DENIED
        IN_PROGRESS =  vn_edu_request.IN_PROGRESS

    class RequestTypeChoices(models.IntegerChoices):
        Late_Add_drop = vn_edu_request.Late_Add_drop
        EMPLOYMENT_IN_EDUCATION = vn_edu_request.EMPLOYMENT_IN_EDUCATION
        REGISTERING = vn_edu_request.REGISTERING
        APPEAL = vn_edu_request.APPEAL
        DELETE_STUDENT_SEMESTER = vn_edu_request.DELETE_STUDENT_SEMESTER
        STUDENT_EMERGENCY_REMOVAL = vn_edu_request.STUDENT_EMERGENCY_REMOVAL

    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                verbose_name=vn_edu_request.STUDENT_REQUEST_STUDENT)
    term = models.ForeignKey('EduTerm.Term', on_delete=models.PROTECT, verbose_name=vn_edu_request.STUDENT_REQUEST_TERM)
    course_term = models.ForeignKey('EduTerm.CourseTerm', on_delete=models.PROTECT,
                                    verbose_name=vn_edu_request.STUDENT_REQUEST_COURSE_TERM)
    request_description = models.TextField(verbose_name=vn_edu_request.STUDENT_REQUEST_REQUEST_DESCRIPTION)
    answer = models.TextField(verbose_name=vn_edu_request.STUDENT_REQUEST_ANSWER)
    status = models.IntegerField(choices=StatusChoices.choices, verbose_name=vn_edu_request.STUDENT_REQUEST_STATUS)
    has_academic_year = models.BooleanField(default=False,
                                            verbose_name=vn_edu_request.STUDENT_REQUEST_HAS_ACADEMIC_YEAR)
    user_answer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                    user_answer=vn_edu_request.STUDENT_REQUEST_USER_ANSWER,
                                    limit_choices_to=Q(is_teacher=True) | Q(is_chancellor=True))
    request_type = models.IntegerField(choices=RequestTypeChoices.choices,
                                       verbose_name=vn_edu_request.STUDENT_REQUEST_REQUEST_TYPE)

    objects = StudentRequestManager()


class EnrollmentCertificateManager(models.Manager):
    pass


class EnrollmentCertificate(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                verbose_name=vn_edu_request.ENROLLMENT_CERTIFICATE_STUDENT)
    term = models.ForeignKey('EduTerm.Term', on_delete=models.PROTECT,
                             verbose_name=vn_edu_request.ENROLLMENT_CERTIFICATE_TERM)
    enrollment_certificate_place = models.CharField(
        verbose_name=vn_edu_request.ENROLLMENT_CERTIFICATE_CERTIFICATE_PLACE, max_length=128, )

    objects = EnrollmentCertificateManager()
