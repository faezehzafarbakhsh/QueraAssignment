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
            "message": "User registered successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
