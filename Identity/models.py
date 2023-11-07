import uuid

from django.contrib.auth import models as user_models

from django.db import models
import variable_names as vn_identity
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model


# Create your user_models here.

def user_portrait_dir_path(instance, file_name):
    return 'image/{path}/{id}/{file_name}_{uuid}.{suffix}'.format(
        path='portrait',
        id=instance.pk,
        file_name=instance.pk,
        uuid=uuid.uuid4(),
        suffix=file_name.split(".")[-1],
    )

class UserManager(models.Manager):
    pass


class User(user_models.AbstractUser):

    class GenderChoices(models.IntegerChoices):
        MALE = 1, vn_identity.MALE
        FEMALE = 2, vn_identity.FEMALE

    class MilitaryChoices(models.IntegerChoices):
        DUTIABLE = 1, vn_identity.DUTIABLE
        EXEMPT = 2, vn_identity.EXEMPT

    portrait = models.ImageField(upload_to=user_portrait_dir_path, null=True, blank=True,
                                 verbose_name=vn_identity.PORTRAIT)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=vn_identity.USER_MOBILE)
    gender = models.IntegerField(choices=GenderChoices.choices, null=True, blank=True,
                                 verbose_name=vn_identity.USER_GENDER)
    birth_date = jmodels.jDateField(verbose_name=vn_identity.USER_BIRTH_DATE)
    college = models.ForeignKey('EduBase.College', on_delete=models.PROTECT, verbose_name=vn_identity.USER_COLLEGE)
    edu_field = models.ForeignKey('EduBase.EduField', on_delete=models.PROTECT, verbose_name=vn_identity.USER_EDU_FIELD,
                                  related_name="users")
    is_it_manager = models.BooleanField(default=False, verbose_name=vn_identity.USER_IS_IT_MANAGER)
    is_chancellor = models.BooleanField(default=False, verbose_name=vn_identity.USER_IS_CHANCELLOR)
    national_code = models.CharField(max_length=10, null=True, blank=True, verbose_name=vn_identity.USER_NATIONAL_CODE)
    is_student = models.BooleanField(default=False, verbose_name=vn_identity.USER_IS_STUDENT)
    is_teacher = models.BooleanField(default=False, verbose_name=vn_identity.USER_IS_TEACHER)
    military_service = models.IntegerField(choices=MilitaryChoices.choices, null=True, blank=True,
                                           verbose_name=vn_identity.USER_MILITARY_SERVICE)


class StudentManager(models.Manager):
    pass


class Student(models.Model):

    class AcademicChoices(models.IntegerChoices):
        YES = 1, vn_identity.YES
        NO = 2, vn_identity.NO

    class EntryChoices(models.IntegerChoices):
        YES = 1, vn_identity.YES
        NO = 2, vn_identity.NO

    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                             verbose_name=vn_identity.USER_ID, related_name="students")
    entry_year = jmodels.jDateField(verbose_name=vn_identity.ENTRY_YEAR)
    entry_term = models.IntegerField(
        choices=EntryChoices.choices, verbose_name=vn_identity.ENTRY_TERM)
    average = models.FloatField(verbose_name=vn_identity.AVERAGE)
    academic_year = models.IntegerField(
        choices=AcademicChoices.choices, verbose_name=vn_identity.ACADEMIC_YEAR)
    current_term = models.ForeignKey(
        "EduTerm", on_delete=models.PROTECT, verbose_name=vn_identity.CURRENT_TERM, related_name="students")


class TeacherManager(models.Manager):
    pass


class Teacher(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                             verbose_name=vn_identity.USER_ID, related_name="teachers")
    level = models.CharField(verbose_name=vn_identity.LEVEL, max_length=64)
    expert = models.CharField(verbose_name=vn_identity.EXPERT, max_length=64)
