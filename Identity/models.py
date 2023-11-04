from django.contrib.auth.models import AbstractUser

from variable_names import *
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from django.contrib.auth import models as user_models
from django.utils.translation import gettext_lazy as _
# Create your user_models here.


class UserManager(user_models.EmptyManager):
    pass


class User(AbstractUser):
    
    class GenderChoices(user_models.IntegerChoices):
        MALE = 1, _('مرد')
        FEMALE = 2, _('زن')
        
    class MilitaryChoices(user_models.IntegerChoices):
        MALE = 1, _('مشمول به خدمت')
        FEMALE = 2, _('معاف از خدمت')

    portrait = user_models.ImageField(upload_to='images/', null=True, blank=True, verbose_name=_(PORTRAIT))
    mobile = user_models.CharField(max_length=11, null=True, blank=True, verbose_name=_(MOBILE))
    gender = user_models.IntegerField(choices=GenderChoices.choices, null=True, blank=True, verbose_name=_(GENDER))
    birth_date = jmodels.jDateField(verbose_name=_(BIRTH_DATE)) 
    college_id = user_models.ForeignKey('EduBase.College', on_delete=user_models.PROTECT, verbose_name=_(COLLEGE_ID))  
    edu_field_id = user_models.ForeignKey('EduBase.EducField', on_delete=user_models.PROTECT, verbose_name=_(EDU_FIELD_ID))  
    is_it_manager = user_models.BooleanField(default=False, verbose_name=_(IS_IT_MANAGER))  
    is_chancellor = user_models.BooleanField(default=False, verbose_name=_(IS_CHANCELLOR))  
    national_code = user_models.CharField(max_length=10, null=True, blank=True, verbose_name=_(NATIONAL_CODE))
    is_student = user_models.BooleanField(default=False, verbose_name=_(IS_STUDENT))
    is_teacher = user_models.BooleanField(default=False, verbose_name=_(IS_TEACHER))
    military_service = user_models.IntegerField(choices=MilitaryChoices.choices, null=True, blank=True, verbose_name=_(MILITARY_SERVICE))


class StudentManager(user_models.EmptyManager):
    pass


class Student(user_models.Model):

    class AcademicChoices(user_models.IntegerChoices):
        YES = 1 , _("بله")
        NO = 2 , _("خیر")
    
    class EntryChoices(user_models.IntegerChoices):
        YES = 1 , _("بله")
        NO = 2 , _("خیر")

    user_id = user_models.ForeignKey(get_user_model() , on_delete=user_models.PROTECT , verbose_name = _(USER_ID))
    entry_year = jmodels.jDateField(verbose_name=_(ENTRY_YEAR))
    entry_term= user_models.IntegerField(choices = EntryChoices.choices , verbose_name=_(ENTRY_TERM))
    average = user_models.models.FloatField(verbose_name=_(AVERAGE))
    academic_year= user_models.IntegerField(choices = AcademicChoices.choices , verbose_name=_(ACADEMIC_YEAR))
    current_term = user_models.ForeignKey("EduTerm", on_delete=user_models.PROTECT, verbose_name=_(CURRENT_TERM))

class TeacherManager(user_models.EmptyManager):
    pass


class Teacher(user_models.Model):
    user_id = user_models.ForeignKey(get_user_model() , on_delete=user_models.PROTECT , verbose_name = _(USER_ID))
    level = user_models.CharField(verbose_name=_(LEVEL), max_length=64)
    expert = user_models.CharField(verbose_name=_(EXPERT), max_length=64)
