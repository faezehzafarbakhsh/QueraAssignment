from rest_framework import serializers
from EduTerm import models as edu_term_models

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_term_models.Term
        fields = '__all__'

class CourseTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_term_models.CourseTerm
        fields = '__all__'

