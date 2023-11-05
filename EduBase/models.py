from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from EduBase import variable_names as vn_edu_base

"""درمورد مقاطع و رشته تحصیلی هست
"""


class EduField(models.Model):
    class EduGradeChoices(models.IntegerChoices):
        AssociateDegree = 1, _("کاردانی")
        Undergraduate = 2, _("کارشناسی")
        MastersDegree = 3, _("کارشناسی ارشد")
        PHD = 4, _("دکتری")

    name = models.CharField(max_length=64, verbose_name=vn_edu_base.EDUFIELD_NAME)
    edu_group = models.CharField(max_length=64, verbose_name=vn_edu_base.EDUFIELD_EDU_GROUP)
    unit_count = models.IntegerField(default=1, validators=[MaxValueValidator(999), MinValueValidator(1)], verbose_name=vn_edu_base.EDUFIELD_UNIT_COUNT)
    edu_grade = models.IntegerField(choices=EduGradeChoices.choices, verbose_name=vn_edu_base.EDUFIELD_EDU_GRADE)


"""در مورد درس ها و دانشگاههایی که اون درس رو ارایه میده 
"""


class Course(models.Model):
    class CourseTypeChoices(models.IntegerChoices):
        General = 1, _("عمومی")
        Specialized = 2, _("تخصصی")
        Basic = 3, _("پایه")
        Optional = 4, _("اختیاری")

    name = models.CharField(max_length=64, verbose_name=vn_edu_base.COURSE_NAME)
    college = models.ForeignKey('EduBase.College', on_delete=models.PROTECT, related_name='courses', verbose_name=vn_edu_base.COURSE_COLLEGE)
    unit_count = models.IntegerField(verbose_name=vn_edu_base.COURSE_UNIT_COUNT)
    course_type = models.IntegerField(choices=CourseTypeChoices.choices, verbose_name=vn_edu_base.COURSE_COURSE_TYPE)


"""در مورد هم نیاز و پیش نیاز و رابطه ای که درس ها باهم دارند
"""


class CourseRelation(models.Model):
    class RelationTypeChoices(models.IntegerChoices):
        TheNeed = 1, _("هم نیاز")
        prerequisite = 2, _("پیش نیاز")

    primary_course = models.ForeignKey('EduBase.Course', on_delete=models.PROTECT, related_name='course_relation_primary_courses', verbose_name=vn_edu_base.COURSERELATION_PRIMARY_COURSE)
    secondary_course = models.ForeignKey('EduBase.Course', on_delete=models.PROTECT, related_name='course_relation_secondary_courses', verbose_name=vn_edu_base.COURSERELATION_SECONDARY_COURSE)
    relation_type = models.IntegerField(choices=RelationTypeChoices.choices, verbose_name=vn_edu_base.COURSERELATION_RELATION_TYPE)


class College(models.Model):
    name = models.CharField(max_length=64, verbose_name=vn_edu_base.COLLEGE_NAME)
