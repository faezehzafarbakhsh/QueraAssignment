from django.http import Http404
from django.shortcuts import render , get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny

from EduRequest import serializers as edu_request_serializers
from EduRequest import models as edu_request_models
from Identity import models as identity_models
from EduTerm import models as edu_term_models


class StudentRequestListView():
    pass


class StudentRequestCreateView():
    pass


class StudentRequestDeleteView():
    pass


class StudentRequestUpdateView():
    pass


class EnrollmentCertificateListView():
    pass


# class StudentRequestListCreateView(generics.ListCreateAPIView):
#     serializer_class = edu_request_serializers.StudentRequestSerializer
#     queryset = edu_request_models.StudentRequest.objects.all()
#     http_method_names = ['get' , 'post']
#     permission_classes = (AllowAny,)
    
# class StudentRequestRetrieveUpdateDestroyView(generics.RetrieveDestroyAPIView):
#     serializer_class = edu_request_serializers.StudentRequestSerializer
#     queryset = edu_request_models.StudentRequest.objects.all()
#     http_method_names = ['get' , 'put' , 'delete']
#     permission_classes = (AllowAny,)
    

class EnrollmentCertificateListCreateView(generics.ListAPIView):
    serializer_class = edu_request_serializers.EnrollmentCertificateSerializer
    queryset = edu_request_models.EnrollmentCertificate.objects.all()
    http_method_names = ['get' , 'post']
    permission_classes = (AllowAny,)
    
class EnrollmentCertificateRetrieveUpdateDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = edu_request_serializers.EnrollmentCertificateSerializer
    queryset = edu_request_models.EnrollmentCertificate.objects.all()
    http_method_names = ['get' , 'put' , 'delete']
    permission_classes = (AllowAny,)
    

class AppealAgainstCourseCreateview(generics.CreateAPIView):
    serializer_class = edu_request_serializers.AppealAgainstCourseSerializer
    queryset = edu_request_models.StudentRequest.objects.filter(request_type = 4)
    http_method_names = ['get' , 'post']
    permission_classes = (AllowAny,)
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_term = get_object_or_404(edu_term_models.CourseTerm, pk=self.kwargs.get('course_term_pk'))
        extra_context = {
            'student': self.request.user,
            'term': course_term.term,
            'course_term': course_term,
        }
        context.update(extra_context)
        return context
    
    def perform_create(self, serializer):
        context = self.get_serializer_context()
        serializer.validated_data['student'] = context.get('student')
        serializer.validated_data['term'] = context.get('term')
        serializer.validated_data['course_term'] = context.get('course_term')
        return super().perform_create(serializer)

class  AppealAgainstCourseListCreateview(generics.ListCreateAPIView):
    serializer_class = edu_request_serializers.StudentRequestSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_term = get_object_or_404(edu_term_models.CourseTerm, pk=self.kwargs.get('course_term_pk'))
        student = identity_models.User.objects.get_student_by_id(self.kwargs.get('pk'))
        if not student:
            raise Http404
        extra_context = {
            'student': student,
            'term': course_term.term,
            'course_term': course_term,
            'request_type': 4,
        }
        context.update(extra_context)
        return context
    
    def perform_create(self, serializer):
        context = self.get_serializer_context()
        serializer.validated_data['student'] = context.get('student')
        serializer.validated_data['term'] = context.get('term')
        serializer.validated_data['course_term'] = context.get('course_term')
        serializer.validated_data['request_type'] = context.get('request_type')
        return super().perform_create(serializer)
    











