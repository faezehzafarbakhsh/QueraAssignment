from django.contrib.auth import models as user_models

from django.db import models 
import variable_names as vn_identity 
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your user_models here.


class UserManager(models.Manager):
    pass


class User(user_models.AbstractUser):
    
    class GenderChoices(models.IntegerChoices):
        MALE = 1, _(vn_identity.MALE)
        FEMALE = 2, _(vn_identity.FEMALE)
        
    class MilitaryChoices(models.IntegerChoices):
        DUTIABLE  = 1, _(vn_identity.DUTIABLE)
        EXEMPT = 2, _(vn_identity.EXEMPT)

    portrait = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name=_(vn_identity.PORTRAIT))
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=_(vn_identity.MOBILE))
    gender = models.IntegerField(choices=GenderChoices.choices, null=True, blank=True, verbose_name=_(vn_identity.GENDER))
    birth_date = jmodels.jDateField(verbose_name=_(vn_identity.BIRTH_DATE)) 
    college_id = models.ForeignKey('EduBase.College', on_delete=models.PROTECT, verbose_name=_(vn_identity.COLLEGE_ID))  
    edu_field_id = models.ForeignKey('EduBase.EducField', on_delete=models.PROTECT, verbose_name=_(vn_identity.EDU_FIELD_ID))  
    is_it_manager = models.BooleanField(default=False, verbose_name=_(vn_identity.IS_IT_MANAGER))  
    is_chancellor = models.BooleanField(default=False, verbose_name=_(vn_identity.IS_CHANCELLOR))  
    national_code = models.CharField(max_length=10, null=True, blank=True, verbose_name=_(vn_identity.NATIONAL_CODE))
    is_student = models.BooleanField(default=False, verbose_name=_(vn_identity.IS_STUDENT))
    is_teacher = models.BooleanField(default=False, verbose_name=_(vn_identity.IS_TEACHER))
    military_service = models.IntegerField(choices=MilitaryChoices.choices, null=True, blank=True, verbose_name=_(vn_identity.MILITARY_SERVICE))


class StudentManager(models.Manager):
    pass


class Student(models.Model):

    class AcademicChoices(models.IntegerChoices):
        YES = 1 , _(vn_identity.YES)
        NO = 2 , _(vn_identity.NO)
    
    class EntryChoices(models.IntegerChoices):
        YES = 1 , _(vn_identity.YES)
        NO = 2 , _(vn_identity.NO)

    user_id = models.ForeignKey(get_user_model() , on_delete=models.PROTECT , verbose_name = _(vn_identity.USER_ID))
    entry_year = jmodels.jDateField(verbose_name=_(vn_identity.ENTRY_YEAR))
    entry_term= models.IntegerField(choices = EntryChoices.choices , verbose_name=_(vn_identity.ENTRY_TERM))
    average = models.models.FloatField(verbose_name=_(vn_identity.AVERAGE))
    academic_year= models.IntegerField(choices = AcademicChoices.choices , verbose_name=_(vn_identity.ACADEMIC_YEAR))
    current_term = models.ForeignKey("EduTerm", on_delete=models.PROTECT, verbose_name=_(vn_identity.CURRENT_TERM))

class TeacherManager(models.Manager):
    pass


class Teacher(models.Model):
    user_id = models.ForeignKey(get_user_model() , on_delete=models.PROTECT , verbose_name = _(vn_identity.USER_ID))
    level = models.CharField(verbose_name=_(vn_identity.LEVEL), max_length=64)
    expert = models.CharField(verbose_name=_(vn_identity.EXPERT), max_length=64)
