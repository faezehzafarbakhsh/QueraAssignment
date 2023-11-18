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

    def validate(self, data):
        """
        Check if the college selected for the course matches the chancellor's college.
        """
        request = self.context.get('request')

        user = request.user
        
        if user.is_chancellor:
            chancellor_college = user.college
            selected_college = data.get('college')
            
            if selected_college != chancellor_college:
                raise serializers.ValidationError(
                    "دانشکده انتخاب شده باید با دانشکده معاون آموزشی یکی باشد.")

        return data


class CourseRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_base_models.CourseRelation
        fields = ['primary_course', 'secondary_course', 'relation_type', ]


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = edu_base_models.College
        fields = ['name', ]
