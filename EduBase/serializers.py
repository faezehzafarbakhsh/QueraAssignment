from rest_framework import serializers
from EduBase import models as edu_base_models


class EduFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_base_models.EduField
        fields = ['name', 'edu_group', 'unit_count', 'edu_grade', ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_base_models.Course
        fields = ['name', 'college', 'unit_count', 'course_type', ]


class CourseRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_base_models.CourseRelation
        fields = ['primary_course', 'secondary_course', 'relation_type', ]


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_base_models.College
        fields = ['name', ]




