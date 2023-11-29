from django.contrib.auth import get_user_model
from django.core import validators as core_validators
from django.db import models
from django.db.models import Q, Avg

from EduEnroll import variable_names as vn_edu_enroll


class EnrollmentManager(models.Manager):

    def get_last_term_by_student(self, student):
        return self.get_total_approved_term(student).first()

    def get_total_approved_term(self, student):
        return self.filter(Q(student=student) & Q(status=2))


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
    status = models.IntegerField(choices=StatusChoices.choices, verbose_name=vn_edu_enroll.ENROLLMENT_STATUS, default=1)
    teacher_assistant_description = models.TextField(verbose_name=vn_edu_enroll.ENROLLMENT_TEACHER_ASISTANT_DESCRIPTION)
    taken_term_number = models.IntegerField(verbose_name=vn_edu_enroll.ENROLLMENT_TAKEN_TERM_NUMBER)

    objects = EnrollmentManager()


class StudentCourseManager(models.Manager):
    def get_not_passed_pre_request_course_by_student_exists(self, student, course_relation):
        return self.filter(Q(student=student) & Q(status=3) & ~Q(course_term__course__in=course_relation)).exists()

    def get_passed_course_by_student_exists(self, student, course_term):
        return self.filter(Q(student=student) & Q(status=3) & Q(course_term=course_term)).exists()

    def get_count_of_student_enroll_in_course_capacity(self, course_term):
        return self.filter(course_term__course=course_term).count()

    def get_average_by_term_and_student(self, student, term):
        return self.filter(Q(student=student) & Q(course_term__term=term)).aggregate(Avg('score'))


class StudentCourse(models.Model):
    class StatusChoices(models.IntegerChoices):
        ENROLLED = 1, vn_edu_enroll.STUDENT_COURSE_ENROLLED
        DELETED = 2, vn_edu_enroll.STUDENT_COURSE_DELETED
        COMPLETED = 3, vn_edu_enroll.STUDENT_COURSE_COMPLETED
        ACCEPTED = 4, vn_edu_enroll.STUDENT_COURSE_ACCEPTED

    course_term = models.ForeignKey('EduTerm.CourseTerm', on_delete=models.PROTECT,
                                    verbose_name=vn_edu_enroll.STUDENT_COURSE_COURSE_TERM,
                                    related_name='student_courses')
    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                verbose_name=vn_edu_enroll.STUDENT_COURSE_STUDENT, related_name='student_courses')
    status = models.IntegerField(choices=StatusChoices.choices, verbose_name=vn_edu_enroll.STUDENT_COURSE_STATUS)
    score = models.FloatField(verbose_name=vn_edu_enroll.STUDENT_COURSE_SCORE,
                              validators=[core_validators.MaxValueValidator(100), core_validators.MinValueValidator(0)])

    objects = StudentCourseManager()
