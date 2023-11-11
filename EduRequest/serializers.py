from rest_framework import serializers
from EduRequest import models as edu_request_models

class StudentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_request_models.StudentRequest
        fields = ['student' , 'term' , 'course_term' , 
                  'request_description' , 'answer' , 'status' ,
                  'has_academic_year' , 'user_answer' , 'request_type',]
        

class EnrollmentCertificateSerializer(serializers.ModelSerializer):
    model = edu_request_models.EnrollmentCertificate
    fields = ['student' , 'term' , 'enrollment_certificate_place',]