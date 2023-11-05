from django.db import models 
from django_jalali.db import models as jmodels
import variable_names as vn_EduTerm


'''
TERM MODEL
'''
class TermManager(models.manager):
    pass
class Term(models.Model):
    name = models.CharField(max_length=64,verbose_name=vn_EduTerm.NAME)
    enrollment_start_datetime = jmodels.jdatetime(verbose_name=vn_EduTerm.ENROLLMENT_START_DATETIME)
    enrollment_end_datetime = jmodels.jdatetime(verbose_name=vn_EduTerm.ENROLLMENT_END_DATETIME)
    class_start_datetime = jmodels.jdatetime(verbose_name=vn_EduTerm.CLASS_START_DATETIME)
    class_end_datetime = jmodels.jdatetime(verbose_name=vn_EduTerm.CLASS_END_DATETIME)
    modify_start_datetime = jmodels.jdatetime(verbose_name=vn_EduTerm.MODIFY_START_DATETIME)
    modify_end_datetime = jmodels.jdatetime(verbose_name=vn_EduTerm.MODIFY_END_DATETIME)
    emergency_course_drop_end_datetime = jmodels.jdatetime(verbose_name=vn_EduTerm.EMERGENCY_COURSE_DROP_END_DATETIME)
    exam_start_date =  jmodels.jDateField(verbose_name=vn_EduTerm.EXAM_START_DATE)
    term_end_date =  jmodels.jDateField(verbose_name=vn_EduTerm.TERM_END_DATE)


class CourseTermManager(models.manager):
    pass
class CourseTerm(models.Model):
    course=models.ForeignKey("EduBase.Course", verbose_name=vn_EduTerm.COURSE, on_delete=models.PROTECT)
    term=models.ForeignKey("EduTerm.Term", verbose_name=vn_EduTerm.TERM, on_delete=models.PROTECT)
    class_day=jmodels.jDateField(verbose_name=vn_EduTerm.CLASS_DAY)
    class_time=jmodels.jdatetime(verbose_name=vn_EduTerm.CLASS_TIME)
    exam_datetime=jmodels.jdatetime(verbose_name=vn_EduTerm.EXAM_DATETIME)
    exam_place=models.CharField(max_length=128,verbose_name=vn_EduTerm.EXAM_PLACE)
    teacher=models.ForeignKey("Identity.User", verbose_name=vn_EduTerm.TEACHER, on_delete=models.PROTECT)
    capacity=models.IntegerField(verbose_name=vn_EduTerm.CAPACITY)