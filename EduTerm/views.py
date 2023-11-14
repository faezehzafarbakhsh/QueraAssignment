from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from EduTerm import serializers as edu_term_serializers
from EduTerm import models as edu_term_models
# Create your views here.


class TermListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_term_serializers.TermSerializer
    queryset =edu_term_models.Term.objects.all()
    http_method_names = [ 'get','post', ]
    permission_classes = (AllowAny,)
    
class TermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_term_serializers.TermSerializer
    queryset = edu_term_models.Term.objects.all()
    http_method_names = ['get', 'put', 'delete',]
    permission_classes = (AllowAny,)


class CoursetermFieldListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_term_serializers.CourseTermSerializer
    queryset = edu_term_models.CourseTerm.objects.all()
    http_method_names = ['get', 'post',]
    permission_classes = (AllowAny,)


class  CoursetermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_term_serializers.CourseTermSerializer
    queryset = edu_term_models.CourseTerm.objects.all()
    http_method_names = ['get', 'put', 'delete',]
    permission_classes = (AllowAny,)