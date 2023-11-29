from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from EduTerm import models as ed_term_models
from EduEnroll import models as enroll_models
from EduEnroll import variable_names as vn_edu_enroll

User = get_user_model()


class StudentCreateCourseSelectionSerializer(serializers.Serializer):
    courses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ed_term_models.CourseTerm.objects.all()
    )
    
    def validate(self, data):
        # check that it is the enrollment time
        return data

class StudentCourseSelectionCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = enroll_models.StudentCourse
        fields = ['course_term']
        extra_kwargs = {'course_term': {'read_only':True}}
        