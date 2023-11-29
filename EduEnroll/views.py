from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from EduEnroll import models as enroll_models
from EduTerm import models as term_models
from EduTerm import serializers as term_serializers
from EduEnroll import serializers as enroll_serializers
from Identity import permission_classes as custom_permissions
from .enrollment_methods import EnrollmentValidation

User = get_user_model()


class CreateCourseSelectionView(APIView):
    serializer_class = enroll_serializers.StudentCreateCourseSelectionSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, pk=None):  # Add 'pk' as a parameter here
        serializer = enroll_serializers.StudentCreateCourseSelectionSerializer(
            data=request.data)

        user = None
        if pk:
            user = User.objects.get(id=pk)
        elif request.user:
            user = request.user

        if user is None:
            # Handle the case where the user is not found
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            courses = serializer.validated_data['courses']

            for course in courses:
                enroll_models.StudentCourse.objects.create(
                    course_term=course,
                    student=user,
                    status=1,
                    score=0,
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailCourseSelectionView(generics.ListAPIView):
    serializer_class = term_serializers.CourseTermSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs.get('pk'):
            user = User.objects.get(pk=self.kwargs.get('pk'))
        else:
            user = self.request.user
        queryset = enroll_models.StudentCourse.objects.filter(
            student=user).values_list('course_term', flat=True)
        return term_models.CourseTerm.objects.filter(id__in=queryset)


class CheckCourseSelectionView(generics.GenericAPIView):
    serializer_class = enroll_serializers.StudentCourseSelectionCheckSerializer
    permission_classes = (IsAuthenticated,)

    def get_user(self):
        if self.kwargs.get('pk'):
            user = User.objects.get(pk=self.kwargs.get('pk'))
        else:
            user = self.request.user
        return user

    def get_queryset(self):
        queryset = enroll_models.StudentCourse.objects.filter(
            student=self.get_user())
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.serializer_class(queryset, many=True).data
        return Response(serialized_data)

    def post(self, request, *args, **kwargs):
        user = self.get_user()
        course_terms_ids = enroll_models.StudentCourse.objects.filter(
            student=user).values_list('course_term', flat=True)

        # Initialize the EnrollmentValidation instance
        enrollment_validation = EnrollmentValidation(
            course_term_id_list=course_terms_ids, student=user)

        if enrollment_validation.validate():
            enroll_models.StudentCourse.objects.filter(
                student=user).update(status=enroll_models.StudentCourse.StatusChoices.COMPLETED)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'شما صلاحیت انتخاب  واحد لیست درس های مورد نظر را ندارید.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)
