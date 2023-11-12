from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from EduBase import serializers as edu_base_serializers
from EduBase import models as edu_base_models


class EduFieldListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_base_serializers.EduFieldSerializer
    queryset = edu_base_models.EduField.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (AllowAny,)


class EduFieldRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_base_serializers.EduFieldSerializer
    queryset = edu_base_models.EduField.objects.all()
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (AllowAny,)


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_base_serializers.CourseSerializer
    queryset = edu_base_models.Course.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (AllowAny,)


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_base_serializers.CourseSerializer
    queryset = edu_base_models.Course.objects.all()
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (AllowAny,)


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
    permission_classes = (AllowAny,)


class CollegeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_base_serializers.CollegeSerializer
    queryset = edu_base_models.College.objects.all()
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (AllowAny,)

