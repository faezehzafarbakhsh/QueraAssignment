from rest_framework import serializers
from EduTerm import models as edu_term_models

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_term_models.Term
        fields = ['name','enrollment_start_datetime','enrollment_end_datetime',
                  'class_start_datetime','class_end_datetime','modify_start_datetime',
                  'modify_end_datetime','emergency_course_drop_end_datetime',
                  'exam_start_date','term_end_date',]

class CourseTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_term_models.CourseTerm
        fields = ['course','term','class_day','class_time',
                  'exam_datetime','exam_place','teacher',
                  'capacity',]

