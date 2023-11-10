from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permisson_calss

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
