from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from EduRequest import serializers as edu_request_serializers
from EduRequest import models as edu_request_models



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


class StudentRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_request_serializers.StudentRequestSerializer
    queryset = edu_request_models.StudentRequest.objects.all()
    http_method_names = ['get' , 'post']
    permission_classes = (AllowAny,)
    
class StudentRequestRetrieveUpdateDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = edu_request_serializers.StudentRequestSerializer
    queryset = edu_request_models.StudentRequest.objects.all()
    http_method_names = ['get' , 'put' , 'delete']
    permission_classes = (AllowAny,)
    

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
    
    











