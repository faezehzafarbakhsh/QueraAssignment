from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from EduBase import variable_names as vn_edu_base


class EduFieldManager(models.Manager):
    pass


class EduField(models.Model):
    """
    درمورد مقاطع و رشته تحصیلی هست
    """
    class EduGradeChoices(models.IntegerChoices):
        AssociateDegree = 1, vn_edu_base.EDU_GRADE_ASSOCIATE_DEGREE
        Undergraduate = 2, vn_edu_base.EDU_GRADE_UNDER_GRADUATE
        MastersDegree = 3, vn_edu_base.EDU_GRADE_MASTERS_DEGREE
        PHD = 4, vn_edu_base.EDU_GRADE_PHD

    name = models.CharField(max_length=64, verbose_name=vn_edu_base.EDU_FIELD_NAME,)
    edu_group = models.CharField(max_length=64, verbose_name=vn_edu_base.EDU_FIELD_EDU_GROUP)
    unit_count = models.IntegerField(default=1, validators=[MaxValueValidator(999), MinValueValidator(1)], verbose_name=vn_edu_base.EDU_FIELD_UNIT_COUNT)
    edu_grade = models.IntegerField(choices=EduGradeChoices.choices, verbose_name=vn_edu_base.EDU_FIELD_EDU_GRADE)

    objects = EduFieldManager()


class CourseManager(models.Manager):
    pass


class Course(models.Model):
    """
    در مورد درس ها و دانشگاههایی که اون درس رو ارایه میده
    """
    class CourseTypeChoices(models.IntegerChoices):
        General = 1, vn_edu_base.COURSE_TYPE_GENERAL
        Specialized = 2, vn_edu_base.COURSE_TYPE_SPECIALIZED
        Basic = 3, vn_edu_base.COURSE_TYPE_BASIC
        Optional = 4, vn_edu_base.COURSE_TYPE_OPTIONAL

    name = models.CharField(max_length=64, verbose_name=vn_edu_base.COURSE_NAME)
    college = models.ForeignKey('EduBase.College', on_delete=models.PROTECT, related_name='courses',
                                verbose_name=vn_edu_base.COURSE_COLLEGE)
    unit_count = models.IntegerField(verbose_name=vn_edu_base.COURSE_UNIT_COUNT)
    course_type = models.IntegerField(choices=CourseTypeChoices.choices, verbose_name=vn_edu_base.COURSE_COURSE_TYPE)

    objects = CourseManager()
    
    def __str__(self) -> str:
        return self.name



class CourseRelationManager(models.Manager):
    def get_pre_request_course_relation(self, course_id):
        """
        لیست شناسه دروس پیشنیاز درس انتخابی را برمیگرداند
        :param course_id:
        :return:
        """
        return self.filter(
            Q(relation_type=2) & Q(primary_course_id=course_id)
        ).values_list('secondary_course_id', flat=True)


class CourseRelation(models.Model):
    """
    در مورد هم نیاز و پیش نیاز و رابطه ای که درس ها باهم دارند
    """

    class RelationTypeChoices(models.IntegerChoices):
        SIMULTANEOUS_REQUISITE = 1, vn_edu_base.RELATION_TYPE_SIMULTANEOUS_REQUISITE
        PRE_REQUISITE = 2, vn_edu_base.RELATION_TYPE_PRE_REQUISITE

    primary_course = models.ForeignKey('EduBase.Course', on_delete=models.PROTECT,
                                       related_name='course_relation_primary_courses',
                                       verbose_name=vn_edu_base.COURSE_RELATION_PRIMARY_COURSE)
    secondary_course = models.ForeignKey('EduBase.Course', on_delete=models.PROTECT,
                                         related_name='course_relation_secondary_courses',
                                         verbose_name=vn_edu_base.COURSE_RELATION_SECONDARY_COURSE)
    relation_type = models.IntegerField(choices=RelationTypeChoices.choices,
                                        verbose_name=vn_edu_base.COURSE_RELATION_RELATION_TYPE)

    objects = CourseRelationManager()
    


class CollegeManager(models.Manager):
    pass


class College(models.Model):
    name = models.CharField(max_length=64, verbose_name=vn_edu_base.COLLEGE_NAME)

    objects = CollegeManager()
    
    def __str__(self) -> str:
        return self.name

