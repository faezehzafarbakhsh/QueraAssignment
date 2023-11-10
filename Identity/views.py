from .models import User , Teacher
from rest_framework import generics
from .identity_serializers import TeacherSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


# User Authentication Views
class UserAuthenticationView:
    pass


class UserChangePasswordView:
    pass

# Teacher Management Views


class TeacherListCreateApiView(generics.ListCreateAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response({
            "teacher": TeacherSerializer(teacher).data
        })

class TeacherRetrieveOrRetrieveOrUpdateOrDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Teacher updated successfully.'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Teacher deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# Student Management Views
class StudentListOrCreateView:
    pass


class StudentRetrieveOrUpdateOrDestroyView:
    pass

# Chancellor Management Views


class ChancellorListOrCreateView:
    pass


class ChancellorRetrieveOrUpdateOrDestroyView:
    pass

# College Management Views


class CollegeListOrCreateView:
    pass


class CollegeRetrieveOrUpdateOrDestroyView:
    pass

# Term Management Views


class TermListOrCreateView:
    pass


class TermRetrieveOrUpdateOrDestroyView:
    pass
