import uuid

from django.contrib.auth import models as user_models
from django.contrib.auth.models import UserManager

from django.db import models
from django.db.models import Q

from Identity import variable_names as vn_identity
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


# Create your user_models here.


def user_portrait_dir_path(instance, file_name):
    return 'image/{path}/{id}/{file_name}_{uuid}.{suffix}'.format(
        path='portrait',
        id=instance.pk,
        file_name=instance.pk,
        uuid=uuid.uuid4(),
        suffix=file_name.split(".")[-1],
    )


class UserManager(UserManager):

    def get_student_by_id(self, id):
        query = self.get(id=id, is_student=True)
        return query


class User(user_models.AbstractUser):
    class GenderChoices(models.IntegerChoices):
        DEFAULT = 0, vn_identity.DEFAULT
        MALE = 1, vn_identity.MALE
        FEMALE = 2, vn_identity.FEMALE

    class MilitaryChoices(models.IntegerChoices):
        DEFAULT = 0, vn_identity.DEFAULT
        END_OF_SERVICE_CARD = 1, vn_identity.END_OF_SERVICE_CARD
        MEDICAL_EXEMPTION = 2, vn_identity.MEDICAL_EXEMPTION
        NON_MEDICAL_EXEMPTION = 3, vn_identity.NON_MEDICAL_EXEMPTION
        EDUCATIONAL_EXEMPTION = 4, vn_identity.EDUCATIONAL_EXEMPTION
        CURRENTLY_IN_SERVICE = 5, vn_identity.CURRENTLY_IN_SERVICE

    unique_code = models.CharField(
        default=None, max_length=8, unique=True, editable=False, null=True)
    portrait = models.ImageField(upload_to=user_portrait_dir_path, null=True, blank=True,
                                 verbose_name=vn_identity.USER_PORTRAIT)
    mobile = models.CharField(max_length=11, null=True,
                              blank=True, verbose_name=vn_identity.USER_MOBILE)
    national_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name=vn_identity.USER_NATIONAL_CODE)
    gender = models.IntegerField(
        choices=GenderChoices.choices, verbose_name=vn_identity.USER_GENDER, default=0)
    birth_date = jmodels.jDateField(
        verbose_name=vn_identity.USER_BIRTH_DATE, null=True)
    college = models.ForeignKey('EduBase.College', on_delete=models.PROTECT, null=True, blank=True,
                                verbose_name=vn_identity.USER_COLLEGE, related_name="users")
    edu_field = models.ForeignKey('EduBase.EduField', on_delete=models.PROTECT, null=True, blank=True,
                                  verbose_name=vn_identity.USER_EDU_FIELD, related_name="users")
    is_it_manager = models.BooleanField(
        default=False, verbose_name=vn_identity.USER_IS_IT_MANAGER)
    is_chancellor = models.BooleanField(
        default=False, verbose_name=vn_identity.USER_IS_CHANCELLOR)
    is_student = models.BooleanField(
        default=False, verbose_name=vn_identity.USER_IS_STUDENT)
    is_teacher = models.BooleanField(
        default=False, verbose_name=vn_identity.USER_IS_TEACHER)
    military_service = models.IntegerField(choices=MilitaryChoices.choices, null=True, blank=True,
                                           verbose_name=vn_identity.USER_MILITARY_SERVICE, default=0)

    def save(self, *args, **kwargs):
        # Generate a unique code if it's not already set
        if not self.unique_code:
            self.unique_code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        prefix = 'su' if self.is_student else 'th' if self.is_teacher else 'ch'
        return f'{prefix}-{get_random_string(length=5)}'

    class Meta:
        unique_together = ('email', 'national_code')

    objects = UserManager()


class StudentManager(models.Manager):
    pass


class Student(models.Model):
    class AcademicChoices(models.IntegerChoices):
        YES = 1, vn_identity.YES
        NO = 2, vn_identity.NO

    class EntryChoices(models.IntegerChoices):
        YES = 1, vn_identity.YES
        NO = 2, vn_identity.NO

    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT, verbose_name=vn_identity.STUDENT_USER,
                                related_name="students", limit_choices_to=Q(is_student=True))
    entry_year = jmodels.jDateField(
        verbose_name=vn_identity.STUDENT_ENTRY_YEAR)
    entry_term = models.IntegerField(
        choices=EntryChoices.choices, verbose_name=vn_identity.STUDENT_ENTRY_TERM)
    current_term = models.ForeignKey("EduTerm.Term", on_delete=models.PROTECT,
                                     verbose_name=vn_identity.STUDENT_CURRENT_TERM, related_name="students")
    average = models.FloatField(verbose_name=vn_identity.STUDENT_AVERAGE)
    academic_year = models.IntegerField(
        choices=AcademicChoices.choices, verbose_name=vn_identity.STUDENT_ACADEMIC_YEAR)

    objects = StudentManager()


class TeacherManager(models.Manager):
    pass


class Teacher(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT, verbose_name=vn_identity.TEACHER_USER,
                                related_name="teachers", limit_choices_to=Q(is_teacher=True))
    level = models.CharField(
        verbose_name=vn_identity.TEACHER_LEVEL, max_length=64)
    expert = models.CharField(
        verbose_name=vn_identity.TEACHER_EXPERT, max_length=64)

    objects = TeacherManager()
