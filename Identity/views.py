from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from Identity import serializers as identity_serializers
from Identity import models as identity_models

User = get_user_model()


class UserRegisterIView(generics.CreateAPIView):
    serializer_class = identity_serializers.RegisterSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        # Additional actions after user creation if needed
        # For example, you might want to send a welcome email.
        # This can be done here.

        # Return response with token
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class UserTokenLoginView(generics.CreateAPIView):
    serializer_class = identity_serializers.UserTokenLoginSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        return Response({'message':"کاربر با موفقیت وارد سایت شد."} , status=status.HTTP_200_OK)