from django.db import models
import variable_names as vn_edurequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


# Create your models here.

class StudentRequestManager(models.Manager):
    pass


class StudentRequest(models.Model):

    class StatusChoices(models.IntegerChoices):
        ACCEPT = _('پذیرش')
        DENIED = _('رد شده')
        IN_PROGRESS = _('در حال بررسی')
        

    class RequestTypeChoices(models.IntegerChoices):
        Late_Add_drop = _('درخواست حذف و اضافه')
        EMPLOYMENT_IN_EDUCATION = _('درخواست اشتغال به تحصیل')
        REGISTREING = _("درخواست ثبت نام")
        APPEAL = _('درخواست تجدید نظر')
        DELETE_STUDENT_SEMESTER = _('درخواست حذف ترم')
        STUDENT_EMERGENCY_REMOVAL = _("درخواست حذف اضطراری دانشجو")

    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                verbose_name=vn_edurequest.STUDENT_REQUEST_STUDENT)
    term = models.ForeignKey('EduTerm.Term', on_delete=models.PROTECT,
                             verbose_name=vn_edurequest.STUDENT_REQUEST_TERM)
    course_term = models.ForeignKey(
        'EduTerm.CourseTerm', on_delete=models.PROTECT, verbose_name=vn_edurequest.STUDENT_REQUEST_COURSE_TERM)
    request_description = models.TextField(
        verbose_name=vn_edurequest.STUDENT_REQUEST_REQUEST_DESCRIPTION)
    answer = models.TextField(verbose_name=vn_edurequest.STUDENT_REQUEST_ANSWER)
    status = models.IntegerField(
        choices=StatusChoices.choices, verbose_name=vn_edurequest.STUDENT_REQUEST_STATUS)
    has_academic_year = models.BooleanField(
        default=False, verbose_name=vn_edurequest.STUDENT_REQUEST_HAS_ACADEMIC_YEAR)
    user_answer = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, user_answer=vn_edurequest.STUDENT_REQUEST_USER_ANSWER)
    request_type = models.IntegerField(
        choices=RequestTypeChoices.choices, verbose_name=vn_edurequest.STUDENT_REQUEST_REQUEST_TYPE)


class EnrollmentCertificateManager(models.Manager):
    pass


class EnrollmentCertificate(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                verbose_name=vn_edurequest.ENROLLMENTCERTIFICATE_STUDENT)
    term = models.ForeignKey('EduTerm.Term', on_delete=models.PROTECT,
                             verbose_name=vn_edurequest.ENROLLMENTCERTIFICATE_TERM)
    enrollment_certificate_place = models.CharField(
        max_length=128, verbose_name=vn_edurequest.ENROLLMENTCERTIFICATE_CERTIFICATE_PLACE)
