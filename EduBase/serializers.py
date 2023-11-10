from rest_framework import serializers
from EduBase import models as edu_base_models


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_base_models.College
        fields = ['name', ]


class EduFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_base_models.EduField
        fields = ['name', 'edu_group', 'unit_count', 'edu_grade', ]

