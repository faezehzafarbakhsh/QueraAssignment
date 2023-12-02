from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from EduTerm import serializers as edu_term_serializers
from EduTerm import models as edu_term_models
from Identity import permission_classes

'''ADDING FILTRIES
'''
from EduTerm import filters as EDUTerm_FILTERS
from django_filters import rest_framework as filters
# Create your views here.


class TermListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_term_serializers.TermSerializer
    queryset = edu_term_models.Term.objects.all()
    http_method_names = ['get', 'post', ]
    permission_classes = (IsAuthenticated, permission_classes.IsItManager)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EDUTerm_FILTERS.TermFilters
    

class TermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_term_serializers.TermSerializer
    queryset = edu_term_models.Term.objects.all()
    http_method_names = ['get', 'put', 'delete',]
    permission_classes = (IsAuthenticated, permission_classes.IsItManager)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EDUTerm_FILTERS.TermFilters

class CoursetermFieldListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_term_serializers.CourseTermSerializer
    queryset = edu_term_models.CourseTerm.objects.all()
    http_method_names = ['get', 'post',]
    permission_classes = (
        IsAuthenticated, permission_classes.IsItManager | permission_classes.IsChancellor)


class CoursetermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_term_serializers.CourseTermSerializer
    http_method_names = ['get', 'put', 'delete',]
    permission_classes = (IsAuthenticated, permission_classes.IsItManager |
                          permission_classes.IsChancellor)

    def get_queryset(self):
        if self.request.user.is_chancellor:
            college = self.request.user.college 

            if college:
                queryset = edu_term_models.CourseTerm.objects.filter(
                    college=college)
            else:
                queryset = edu_term_models.CourseTerm.objects.none()
        else:
            queryset = edu_term_models.CourseTerm.objects.all()

        return queryset
