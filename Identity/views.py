from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from .models import Teacher, User
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# Create your views here.


# User Authentication Views
class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


class UserAuthenticationView:
    pass


class UserChangePasswordView:
    pass

# Teacher Management Views


class TeacherListCreateApiView(generics.ListCreateAPIView):
    pass
#     serializer_class = TeacherSerializer

#     queryset = Teacher.objects.all()

#     def create(self, request):

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)


class TeacherUpdateOrDestroyView:
    pass

# Student Management Views


class StudentRetrieveOrCreateView:
    pass


class StudentUpdateOrDestroyView:
    pass

# Chancellor Management Views


class ChancellorRetrieveOrCreateView:
    pass


class ChancellorUpdateOrDestroyView:
    pass

# College Management Views


class CollegeRetrieveOrCreateView:
    pass


class CollegeUpdateOrDestroyView:
    pass

# Term Management Views


class TermRetrieveOrCreateView:
    pass


class TermUpdateOrDestroyView:
    pass
