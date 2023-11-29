from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django_jalali.db import models as jmodels
from EduTerm import variable_names as vn_edu_term


'''
TERM MODEL
'''


class TermManager(models.Manager):
    pass


class Term(models.Model):
    name = models.CharField(max_length=64, verbose_name=vn_edu_term.TERM_NAME)
    enrollment_start_datetime = jmodels.jDateTimeField(verbose_name=vn_edu_term.TERM_ENROLLMENT_START_DATETIME)
    enrollment_end_datetime = jmodels.jDateTimeField(verbose_name=vn_edu_term.TERM_ENROLLMENT_END_DATETIME)
    class_start_datetime = jmodels.jDateTimeField(verbose_name=vn_edu_term.TERM_CLASS_START_DATETIME)
    class_end_datetime = jmodels.jDateTimeField(verbose_name=vn_edu_term.TERM_CLASS_END_DATETIME)
    modify_start_datetime = jmodels.jDateTimeField(verbose_name=vn_edu_term.TERM_MODIFY_START_DATETIME)
    modify_end_datetime = jmodels.jDateTimeField(verbose_name=vn_edu_term.TERM_MODIFY_END_DATETIME)
    emergency_course_drop_end_datetime = jmodels.jDateTimeField(
        verbose_name=vn_edu_term.TERM_EMERGENCY_COURSE_DROP_END_DATETIME)
    exam_start_date = jmodels.jDateField(verbose_name=vn_edu_term.TERM_EXAM_START_DATE)
    term_end_date = jmodels.jDateField(verbose_name=vn_edu_term.TERM_TERM_END_DATE)
    active_term = models.BooleanField(default=False, verbose_name=vn_edu_term.TERM_ACTIVE_TERM)

    objects = TermManager()


class CourseTermManager(models.Manager):
    def get_course_term_by_list_id(self, course_term_id):
        return self.filter(pk__in=course_term_id)


class CourseTerm(models.Model):
    course = models.ForeignKey("EduBase.Course", verbose_name=vn_edu_term.COURSE_TERM_COURSE, on_delete=models.PROTECT,
                               related_name='course_terms')
    term = models.ForeignKey("EduTerm.Term", verbose_name=vn_edu_term.COURSE_TERM_TERM, on_delete=models.PROTECT,
                             related_name='course_terms')
    class_day = jmodels.jDateField(verbose_name=vn_edu_term.COURSE_TERM_CLASS_DAY)
    class_time = jmodels.jDateTimeField(verbose_name=vn_edu_term.COURSE_TERM_CLASS_TIME)
    exam_datetime = jmodels.jDateTimeField(verbose_name=vn_edu_term.COURSE_TERM_EXAM_DATETIME)
    exam_place = models.CharField(max_length=128, verbose_name=vn_edu_term.COURSE_TERM_EXAM_PLACE)
    teacher = models.ForeignKey(get_user_model(), verbose_name=vn_edu_term.COURSE_TERM_TEACHER,
                                on_delete=models.PROTECT, related_name='course_terms',
                                limit_choices_to=Q(is_teacher=True))
    capacity = models.IntegerField(verbose_name=vn_edu_term.COURSE_TERM_CAPACITY)

    objects = CourseTermManager()
