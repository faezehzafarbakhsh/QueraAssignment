from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from EduBase import serializers as edu_base_serializers
from EduBase import models as edu_base_models
from Identity import permission_classes
from EduBase import filters as edu_base_filter
from django_filters import rest_framework as filters

class EduFieldListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_base_serializers.EduFieldSerializer
    queryset = edu_base_models.EduField.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (permission_classes.IsItManager,)


class EduFieldRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_base_serializers.EduFieldSerializer
    queryset = edu_base_models.EduField.objects.all()
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (permission_classes.IsItManager,)


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_base_serializers.CourseSerializer
    queryset = edu_base_models.Course.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (
        IsAuthenticated, permission_classes.IsItManager | permission_classes.IsChancellor)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = (edu_base_filter.ListCourseFilter, edu_base_filter.ListCourseTermFilter)


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_base_serializers.CourseSerializer
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (IsAuthenticated, permission_classes.IsItManager |
                          permission_classes.IsChancellor)

    def get_queryset(self):
        if self.request.user.is_chancellor:
            college = self.request.user.college 

            if college:
                queryset = edu_base_models.Course.objects.filter(
                    college=college)
            else:
                queryset = edu_base_models.Course.objects.none()
        else:
            queryset = edu_base_models.Course.objects.all()

        return queryset


class CourseRelationListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_base_serializers.CourseRelationSerializer
    queryset = edu_base_models.CourseRelation.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (AllowAny,)


class CourseRelationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_base_serializers.CourseRelationSerializer
    queryset = edu_base_models.Course.objects.all()
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (AllowAny,)


class CollegeListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_base_serializers.CollegeSerializer
    queryset = edu_base_models.College.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated, permission_classes.IsItManager)


class CollegeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_base_serializers.CollegeSerializer
    queryset = edu_base_models.College.objects.all()
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (IsAuthenticated, permission_classes.IsItManager)
