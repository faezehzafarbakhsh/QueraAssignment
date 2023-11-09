from django.contrib.auth import get_user_model
from django.core import validators as core_validators
from django.db import models
from django.db.models import Q

from EduEnroll import variable_names as vn_edu_enroll


class EnrollmentManager(models.Manager):
    pass


class Enrollment(models.Model):
    class StatusChoices(models.IntegerChoices):
        PENDING = 1, vn_edu_enroll.ENROLLMENT_PENDING
        APPROVED = 2, vn_edu_enroll.ENROLLMENT_APPROVED
        REJECTED = 3, vn_edu_enroll.ENROLLMENT_REJECTED

    term = models.ForeignKey('EduTerm.Term', on_delete=models.PROTECT, verbose_name=vn_edu_enroll.ENROLLMENT_TERM,
                             related_name='enrollments')
    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, limit_choices_to=Q(is_student=True),
                                verbose_name=vn_edu_enroll.ENROLLMENT_STUDENT, related_name='enrollment_students')
    teacher_assistant = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                          limit_choices_to=Q(is_teacher=True),
                                          verbose_name=vn_edu_enroll.ENROLLMENT_TEACHER_ASISTANT,
                                          related_name='enrollment_teacher_assistants')
    status = models.CharField(choices=StatusChoices.choices, verbose_name=vn_edu_enroll.ENROLLMENT_STATUS, default=1)
    teacher_assistant_description = models.TextField(verbose_name=vn_edu_enroll.ENROLLMENT_TEACHER_ASISTANT_DESCRIPTION)
    taken_term_number = models.IntegerField(verbose_name=vn_edu_enroll.ENROLLMENT_TAKEN_TERM_NUMBER)

    objects = EnrollmentManager()


class StudentCourseManager(models.Manager):
    pass


class StudentCourse(models.Model):
    class StatusChoices(models.IntegerChoices):
        ENROLLED = 1, vn_edu_enroll.STUDENT_COURSE_ENROLLED
        DELETED = 2, vn_edu_enroll.STUDENT_COURSE_DELETED
        COMPLETED = 3, vn_edu_enroll.STUDENT_COURSE_COMPLETED

    course_term = models.ForeignKey('EduTerm.CourseTerm', on_delete=models.PROTECT,
                                    verbose_name=vn_edu_enroll.STUDENT_COURSE_COURSE_TERM,
                                    related_name='student_courses')
    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                verbose_name=vn_edu_enroll.STUDENT_COURSE_STUDENT, related_name='student_courses')
    status = models.CharField(choices=StatusChoices.choices, verbose_name=vn_edu_enroll.STUDENT_COURSE_STATUS)
    score = models.FloatField(verbose_name=vn_edu_enroll.STUDENT_COURSE_SCORE,
                              validators=[core_validators.MaxValueValidator(100), core_validators.MinValueValidator(0)])

    objects = StudentCourseManager()
