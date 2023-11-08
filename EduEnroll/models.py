from django.db import models
import variable_names as translate

class Enrollment(models.Model):
    STATUS_CHOICES = (
        (translate.PENDING, translate.PENDING),
        (translate.APPROVED, translate.APPROVED),
        (translate.REJECTED, translate.REJECTED),
    )
    id = models.AutoField(primary_key=True, unique=True)
    term = models.ForeignKey('Term', verbose_name=translate.TERM)
    student = models.ForeignKey('Student', verbose_name=translate.STUDENT)
    teacher_assistant = models.ForeignKey('Teacher', verbose_name=translate.TEACHERASISTANT)
    status = models.CharField(choices=STATUS_CHOICES, verbose_name=translate.STATUS)
    teacher_assistant_description = models.TextField(verbose_name=translate.TEACHER_ASISTANT_DESCRIPTION)
    taken_term_number = models.IntegerField(verbose_name=translate.TAKEN_TERM_NUMBER)

class StudentCourse(models.Model):
    STATUS_CHOICES = (
        (translate.ENROLLED, translate.ENROLLED),
        (translate.DELETED, translate.DELETED),
        (translate.COMPLETED, translate.COMPLETED),
    )
    id = models.AutoField(primary_key=True)
    course_term = models.ForeignKey('CourseTerm', verbose_name=translate.COURSE_TERM)
    student = models.ForeignKey("Student", verbose_name=translate.STUDENT)
    status = models.CharField(choices=STATUS_CHOICES, verbose_name=translate.STATUS)
    score = models.FloatField(verbose_name=translate.SCORE, min=0, max=100)