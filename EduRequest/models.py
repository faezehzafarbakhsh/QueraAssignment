from django.db import models
from django.db.models import Q

from EduRequest import variable_names as vn_edu_request
from django.contrib.auth import get_user_model


# Create your models here.

class StudentRequestManager(models.Manager):
    pass


class StudentRequest(models.Model):
    class StatusChoices(models.IntegerChoices):
        ACCEPT = 1, vn_edu_request.ACCEPT
        DENIED = 2, vn_edu_request.DENIED
        IN_PROGRESS = 3, vn_edu_request.IN_PROGRESS

    class RequestTypeChoices(models.IntegerChoices):
        LATE_ADD_DROP = 1, vn_edu_request.LATE_ADD_DROP
        EMPLOYMENT_IN_EDUCATION = 2, vn_edu_request.EMPLOYMENT_IN_EDUCATION
        REGISTERING = 3, vn_edu_request.REGISTERING
        APPEAL = 4, vn_edu_request.APPEAL
        DELETE_STUDENT_SEMESTER = 5, vn_edu_request.DELETE_STUDENT_SEMESTER
        STUDENT_EMERGENCY_REMOVAL = 6, vn_edu_request.STUDENT_EMERGENCY_REMOVAL

    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                verbose_name=vn_edu_request.STUDENT_REQUEST_STUDENT,
                                related_name='student_requests')
    term = models.ForeignKey('EduTerm.Term', on_delete=models.PROTECT, verbose_name=vn_edu_request.STUDENT_REQUEST_TERM,
                            related_name='student_requests')
    course_term = models.ForeignKey('EduTerm.CourseTerm', on_delete=models.PROTECT,
                                    verbose_name=vn_edu_request.STUDENT_REQUEST_COURSE_TERM,
                                    related_name='student_requests')
    request_description = models.TextField(verbose_name=vn_edu_request.STUDENT_REQUEST_REQUEST_DESCRIPTION)
    answer = models.TextField(verbose_name=vn_edu_request.STUDENT_REQUEST_ANSWER)
    status = models.IntegerField(choices=StatusChoices.choices, verbose_name=vn_edu_request.STUDENT_REQUEST_STATUS,
                                 default=None)
    has_academic_year = models.BooleanField(default=False,
                                            verbose_name=vn_edu_request.STUDENT_REQUEST_HAS_ACADEMIC_YEAR)
    user_answer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                    verbose_name=vn_edu_request.STUDENT_REQUEST_USER_ANSWER,
                                    limit_choices_to=Q(is_teacher=True) | Q(is_chancellor=True),
                                    related_name='student_request_answers', null=True, blank=True)
    request_type = models.IntegerField(choices=RequestTypeChoices.choices,
                                    verbose_name=vn_edu_request.STUDENT_REQUEST_REQUEST_TYPE)

    objects = StudentRequestManager()


class EnrollmentCertificateManager(models.Manager):
    pass


class EnrollmentCertificate(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                verbose_name=vn_edu_request.ENROLLMENT_CERTIFICATE_STUDENT,
                                related_name='enrollment_certificates')
    term = models.ForeignKey('EduTerm.Term', on_delete=models.PROTECT,
                             verbose_name=vn_edu_request.ENROLLMENT_CERTIFICATE_TERM,
                             related_name='enrollment_certificates'
                             )
    enrollment_certificate_place = models.CharField(
        verbose_name=vn_edu_request.ENROLLMENT_CERTIFICATE_CERTIFICATE_PLACE, max_length=128, default=None)
    status = models.IntegerField(choices=StudentRequest.StatusChoices.choices,
                                 verbose_name=vn_edu_request.STUDENT_REQUEST_STATUS, default=3)

    objects = EnrollmentCertificateManager()
