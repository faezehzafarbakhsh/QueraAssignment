from rest_framework import serializers
from EduRequest import models as edu_request_models
from EduTerm import models as edu_term_models


class StudentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_request_models.StudentRequest
        fields = ['request_description', 'request_type']
        extra_kwargs = {'request_type': {'read_only': True}}


class EnrollmentCertificateSerializer(serializers.ModelSerializer):
    model = edu_request_models.EnrollmentCertificate
    fields = ['student', 'term', 'enrollment_certificate_place',]


class TeacherAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_request_models.StudentRequest
        fields = ['status', 'request_description', 'answer']


# class  EDUTERM_CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = edu_term_models.CourseTerm
#         fields = ['course' , ]


# class AppealAgainstCourseSerializer(serializers.ModelSerializer):
#     course = EDUTERM_CourseSerializer()
#     class Meta:
#         model = edu_request_models.StudentRequest
#         fields = ['student' , 'course' , 'request_description' , 'answer', ]
