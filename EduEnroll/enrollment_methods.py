from EduBase import models as edu_base_models
from EduEnroll import models as edu_enroll_models
from EduTerm import models as edu_term_models


class EnrollmentValidation:

    def __init__(self, course_term_id_list, student):
        self.course_term_id_list = course_term_id_list
        self.course_term_list = edu_term_models.CourseTerm.objects.get_course_term_by_list_id(course_term_id_list)
        self.student = student

    def validate(self):
        """
        در این بخش لیست کامل بررسی ها به ترتیب برای هر درس بررسی می‌شود.
        درصورتیکه یکی از دروس خطا بدهد می‌توان عملیات را متوقف کرد.
        :return:
        """
        course_dict = {}
        course_check = []
        for course_term in self.course_term_list:
            check = self.has_course_relation_passed(course_term=course_term) and self.has_course_duplicate() and\
                    self.has_course_passed(course_term) and self.has_course_has_capacity(course_term) and\
                    self.has_can_permission_to_get_24_unit() and self.has_different_course_exam_time() and\
                    self.has_different_course_exam_time() and self.has_different_class_time() and\
                    self.has_academic_year() and self.has_course_in_field(course_term)
            course_dict[course_term.pk] = check
            course_check.append(check)

        return set(course_check) == 1

    def has_course_relation_passed(self, course_term):
        """
        دریافت پیش‌نیازهای درس
        بررسی اینکه دانشجو همه پیش‌نیازها را پاس کرده یا نه
        :return: Bool
        """
        course_relation = edu_base_models.CourseRelation.objects.get_pre_request_course_relation(course_term.course.pk)
        student_course = edu_enroll_models.StudentCourse.objects.get_not_passed_pre_request_course_by_student_exists(
            self.student, course_relation
        )
        return student_course

    def has_course_duplicate(self):
        """
        بررسی اینکه آیا درس انتخابی قبلا در لیست دروس انتخابی هست یا نه
        :return:
        """
        return len(self.course_term_id_list) == len(set(self.course_term_id_list))

    def has_course_passed(self, course_term):
        """
        بررسی اینکه آیا درس انتخابی قبلا پاس شده یا نه
        :return:
        """
        return edu_enroll_models.StudentCourse.objects.get_passed_course_by_student_exists(self.student, course_term)

    def has_course_has_capacity(self, course_term):
        """
        آیا درس انتخابی ظرفیت دارد یا خیر
        :return:
        """
        count_enroll_in_course = edu_enroll_models.StudentCourse.objects.get_count_of_student_enroll_in_course_capacity(course_term)
        return count_enroll_in_course < course_term.capacity

    def has_can_permission_to_get_24_unit(self):
        """
        چک شود درصورتیکه در ترم قبل معدل بالای ۱۷ می‌باشد بتواند ۲۴ واحد بردارد در غیر اینصورت ۲۰ واحد
        معدل ترم قبل دانشجو مشخص می‌شود
        ترم قبل دانشجو عبارت است از آخرین ترمی که در جدول انتخاب واحد در وضعیت تایید شده قرار دارد.
        درصرتیکه معدل بالای ۱۷ باید می‌تواند بیشتر از ۲۴ واحد بردارد.
        :return:
        """
        get_last_term = edu_enroll_models.Enrollment.objects.get_last_term_by_student(student=self.student)
        get_average = edu_enroll_models.StudentCourse.objects.get_average_by_term_and_student(
            student=self.student, term=get_last_term
        )
        return get_average > 17

    def has_different_course_exam_time(self):
        """
        تداخل زمانی امتحان نباید وجود داشته باشد
        :return:
        """
        return True
    def has_different_class_time(self):
        """
        تداخل زمانی کلاس ها وجود نداشته باشد
        :return:
        """
        return True

    def has_academic_year(self):
        """
        تعداد ترم های انتخاب شده دانشجو باید کمتر از تعداد سنوات ثبت شده در بخش دانشجو باشد
        :return:
        """
        get_total_approved_term = edu_enroll_models.Enrollment.objects.get_total_approved_term(self.student)
        return self.student.academic_year >= get_total_approved_term.count()

    def has_course_in_field(self, course_term):
        """
        درس انتخابی بررسی شود که آیا مربوط به رشته انتخابی دانشجو است یا خبر
        درس باید جزو دروس دانشکده باشد
        :return:
        """
        course_college = course_term.course.college
        student_college = self.student.college
        return course_college == student_college


