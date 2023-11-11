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
    