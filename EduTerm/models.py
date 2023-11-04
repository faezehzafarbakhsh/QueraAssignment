from django.db import models 
from django_jalali.db import models as jmodels
from variable_names import *
from django.utils.translation import gettext_lazy as _

'''
TERM MODEL
'''
class TermManager(models.manager):
    pass
class Term(models.Model):
    name = models.CharField(max_length=64,verbose_name=_(Name))
    enrollment_start_datetime = jmodels.jdatetime(verbose_name=_(Enrollment_start_datetime))
    enrollment_end_datetime = jmodels.jDateField(verbose_name=_(Enrollment_end_datetime))
    class_start_datetime = jmodels.jDateField(verbose_name=_(Class_start_datetime))
    class_end_datetime = jmodels.jDateField(verbose_name=_(Class_end_datetime))
    modify_start_datetime = jmodels.jDateField(verbose_name=_(Modify_start_datetime))
    modify_end_datetime = jmodels.jDateField(verbose_name=_(Modify_end_datetime))
    emergency_course_drop_end_datetime = jmodels.jDateField(verbose_name=_(Emergency_course_drop_end_datetime))
    exam_start_date =  jmodels.jDateField(verbose_name=_(Exam_start_date))
    term_end_date =  jmodels.jDateField(verbose_name=_(Term_end_date))


class CourseTermManager(models.manager):
    pass
class CourseTerm(models.Model):
    course=models.ForeignKey("EduBase.Course", verbose_name=_(Course), on_delete=models.PROTECT)
    term=models.ForeignKey("EduTerm", verbose_name=_(Term), on_delete=models.PROTECT)
    class_day=jmodels.jdatetime(verbose_name=_(Class_day))
    class_time=models.DateTimeField(timezone=True,verbose_name=_(Class_time))
    exam_datetime=jmodels.jDateField(verbose_name=_(Exam_datetime))
    exam_place=models.CharField(max_length=128,verbose_name=_(Exam_place))
    teacher=models.ForeignKey("Identity.User", verbose_name=_(Teacher), on_delete=models.PROTECT)
    capacity=models.IntegerField(verbose_name=_(Capacity))