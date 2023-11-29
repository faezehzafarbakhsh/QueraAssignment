from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from EduRequest import serializers as edu_request_serializers
from EduRequest import models as edu_request_models
from Identity import models as identity_models
from EduTerm import models as edu_term_models
from django.contrib.auth import get_user_model
from Identity import permission_classes

User = get_user_model()


class EnrollmentCertificateListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_request_serializers.EnrollmentCertificateSerializer
    queryset = edu_request_models.EnrollmentCertificate.objects.all()
    permission_classes = (permission_classes.IsStudent,)

    def get_queryset(self):
        return edu_request_models.EnrollmentCertificate.objects.filter(student=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        print(self.request.user)
        serializer.context['student'] = self.request.user
        serializer.context['status'] = 3
        return serializer


class EnrollmentCertificateRetrieveUpdateDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = edu_request_serializers.EnrollmentCertificateSerializer
    queryset = edu_request_models.EnrollmentCertificate.objects.all()
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (AllowAny,)

# student


class StudentRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_request_serializers.StudentRequestSerializer
    http_method_names = ['get', 'post']
    permission_classes = (permission_classes.IsStudent,)

    def get_user(self):
        if self.kwargs.get('student_pk'):
            user = User.objects.get(pk=self.kwargs.get('student_pk'))
        else:
            user = self.request.user
        return user

    def get_queryset(self):
        return edu_request_models.StudentRequest.objects.filter(student=self.get_user())

    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_term = get_object_or_404(
            edu_term_models.CourseTerm, pk=self.kwargs.get('course_term_pk'))
        request_type = self.kwargs.get('request_type')
        student = self.get_user()
        if not student:
            raise Http404
        extra_context = {
            'student': student,
            'term': course_term.term,
            'course_term': course_term,
            'request_type': request_type,
            'status': 2,
        }
        context.update(extra_context)
        return context

    def perform_create(self, serializer):
        context = self.get_serializer_context()
        serializer.validated_data['student'] = context.get('student')
        serializer.validated_data['term'] = context.get('term')
        serializer.validated_data['course_term'] = context.get('course_term')
        serializer.validated_data['request_type'] = context.get('request_type')
        serializer.validated_data['status'] = context.get('status')
        return super().perform_create(serializer)


class StudentRequestDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_request_serializers.StudentRequestSerializer
    permission_classes = (permission_classes.IsStudent,)
    
    def get_user(self):
        if self.kwargs.get('student_pk'):
            user = User.objects.get(pk=self.kwargs.get('student_pk'))
        else:
            user = self.request.user
        return user

    def get_queryset(self):
        return edu_request_models.StudentRequest.objects.filter(student=self.get_user())

    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_term = get_object_or_404(
            edu_term_models.CourseTerm, pk=self.kwargs.get('course_term_pk'))
        student = self.request.user
        if not student:
            raise Http404
        extra_context = {
            'student': student,
            'term': course_term.term,
            'course_term': course_term,
        }
        context.update(extra_context)
        return context



# teacher


class TeacherAnswerStudentRequestSerializer(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = edu_request_serializers.TeacherAnswerSerializer
    queryset = edu_request_models.StudentRequest
    permission_classes = (permission_classes.IsTeacher |
                          permission_classes.IsItManager,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_term = get_object_or_404(
            edu_term_models.CourseTerm, pk=self.kwargs.get('course_term_pk'))
        teacher = self.request.user
        if not teacher:
            raise Http404
        extra_context = {
            'answer_user': teacher,
            # Use get with a default value
            'answer': self.request.data.get('answer', ''),
            # Use get with a default value
            'status': self.request.data.get('status', ''),
        }

        context.update(extra_context)
        return context


class Delete_Student_SemesterListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_request_serializers.StudentRequestSerializer
    queryset = edu_request_models.StudentRequest.objects.filter(request_type=5)

    http_method_names = ['get', 'post']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_term = get_object_or_404(
            edu_term_models.CourseTerm, pk=self.kwargs.get('course_term_pk'))
        student = identity_models.User.objects.get_student_by_id(
            self.kwargs.get('pk'))
        if not student:
            raise Http404
        extra_context = {
            'student': student,
            'term': course_term.term,
            'course_term': course_term,
            'request_type': 5,
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


class StudentEmergencyRemovalCreateView(generics.CreateAPIView):
    serializer_class = edu_request_serializers.StudentRequestSerializer
    queryset = edu_request_models.StudentRequest.objects.filter(request_type=6)
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_term = get_object_or_404(
            edu_term_models.CourseTerm, pk=self.kwargs.get('course_term_pk'))
        extra_context = {
            'student': get_user_model().objects.first(),
            'term': course_term.term,
            'course_term': course_term,
            'request_type': 6,
            'status': 1,
        }
        context.update(extra_context)
        return context

    def perform_create(self, serializer):
        context = self.get_serializer_context()
        serializer.validated_data['student'] = context.get('student')
        serializer.validated_data['term'] = context.get('term')
        serializer.validated_data['course_term'] = context.get('course_term')
        serializer.validated_data['request_type'] = context.get('request_type')
        serializer.validated_data['status'] = context.get('status')
        return super().perform_create(serializer)


class StudentEmergencyRemovalListCreateView(generics.ListCreateAPIView):
    serializer_class = edu_request_serializers.StudentRequestSerializer
    queryset = edu_request_models.StudentRequest.objects.filter(request_type=6)

    http_method_names = ['get', 'post']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_term = get_object_or_404(
            edu_term_models.CourseTerm, pk=self.kwargs.get('course_term_pk'))
        student = identity_models.User.objects.get_student_by_id(
            self.kwargs.get('pk'))
        if not student:
            raise Http404
        extra_context = {
            'student': student,
            'term': course_term.term,
            'course_term': course_term,
            'request_type': 6,
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


# class CoursetermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = edu_term_serializers.CourseTermSerializer
#     http_method_names = ['get', 'put', 'delete',]
#     permission_classes = (IsAuthenticated, permission_classes.IsItManager |
#                           permission_classes.IsChancellor)

#     def get_queryset(self):
#         if self.request.user.is_chancellor:
#             college = self.request.user.college if self.request.user.is_chancellor else None

#             if college:
#                 queryset = edu_term_models.CourseTerm.objects.filter(
#                     college=college)
#             else:
#                 queryset = edu_term_models.CourseTerm.objects.none()
#         else:
#             queryset = edu_term_models.CourseTerm.objects.all()

#         return queryset
