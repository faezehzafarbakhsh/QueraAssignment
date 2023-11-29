from rest_framework import serializers
from EduRequest import models as edu_request_models
from EduTerm import models as edu_term_models


class StudentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_request_models.StudentRequest
        fields = ['request_description', 'request_type']
        extra_kwargs = {'request_type': {'read_only': True}}


class TeacherAnswerStudentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_request_models.StudentRequest
        fields = ['id', 'student.id', 'request_type', 'request_description',
                  'term', 'course_term.id', 'answer', 'status']
        extra_kwargs = {
            'id': {'read_only': True},
            'student': {'read_only': True},
            'request_type': {'read_only': True},
            'request_description': {},  # Remove 'read_only'
            'term': {'read_only': True},
            'course_term': {'read_only': True},
        }


class EnrollmentCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_request_models.EnrollmentCertificate
        fields = ['student','term', 'status']
        extra_kwargs = {
            'status': {'read_only': True},
            'student': {'read_only': True},
            }


class TeacherAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_request_models.StudentRequest
        fields = ['status', 'request_description', 'answer']
