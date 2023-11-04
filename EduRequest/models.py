from django.db import models
import variable_names as vn_identity 
from django.utils.translation import gettext_lazy as _


# Create your models here.

class StudentRequestManager(models.Manager):
    pass

class StudentRequest(models.Model):
    
    class StatusChoices(models.IntegerChoices):
        pass
    
    class RequestTypeChoices(models.IntegerChoices):
        pass
    
    student = models.ForeignKey('Identity.User' , on_delete = models.PROTECT , verbose_name=_(vn_identity.STUDENT))
    term = models.ForeignKey('EduTerm.Term' , on_delete = models.PROTECT , verbose_name = _(vn_identity.TERM))
    course_term = models.ForeignKey('EduTerm.CourceTerm' , on_delete=models.PROTECT , verbose_name = _(vn_identity.COURSE_TERM))
    request_description = models.TextField(verbose_name=_(vn_identity.REQUEST_DESCRIPTION))
    answer = models.TextField(verbose_name = _(vn_identity.ANSWER))
    status = models.IntegerField(choices=StatusChoices.choices , verbose_name = _(vn_identity.STATUS))
    has_academic_year = models.BooleanField(default=False , verbose_name = _(vn_identity.HAS_ACADEMIC_YEAR))
    user_answer = models.ForeignKey('Identy.User' , on_delete = models.PROTECT , user_answer = _(vn_identity.USER_ANSWER))
    request_type = models.IntegerField(choices=RequestTypeChoices.choices , verbose_name = _(vn_identity.REQUEST_TYPE))


class EnrollmentCertificateManager(models.Manager):
    pass

class EnrollmentCertificate(models.Model):
    student = models.ForeignKey('Identity.User' , on_delete = models.PROTECT , verbose_name = _(vn_identity.STUDENT))
    term = models.ForeignKey('EduTerm.Term' , on_delete = models.PROTECT , verbose_name = _(vn_identity.TERM))
    enrollment_certificate_place = models.CharField(max_length=128 , verbose_name = _(vn_identity.STUDENT))
    