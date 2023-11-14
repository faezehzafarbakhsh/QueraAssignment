from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import AccessToken

from Identity import models as identity_models
from Identity import serializers as identity_serializers
from Identity import permisson_classes as custom_permissions
from Identity import custom_classes

User = get_user_model()

# Authentication Views


class UserRegisterIView(generics.CreateAPIView):
    """
    View for user registration.

    Args:
        generics (class): Django REST Framework generics class.

    Returns:
        Response: JSON response containing the access token upon successful user registration.
    """
    serializer_class = identity_serializers.RegisterSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserTokenLoginView(generics.CreateAPIView):
    """
    View for user login using JWT token.

    Args:
        generics (class): Django REST Framework generics class.

    Returns:
        Response: JSON response with a success message upon successful user login.
    """
    serializer_class = identity_serializers.UserTokenLoginSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        print(context)
        return context

    def perform_create(self, serializer):
        context = self.get_serializer_context()
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return super().perform_create(serializer)

    def post(self, request, *args, **kwargs):
        return Response({"message": "کاربر با موفقیت وارد سایت شد."}, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'یوزر با موفقیت از سایت خارج شد.'}, status=status.HTTP_200_OK)


class ChangePasswordRequestView(generics.CreateAPIView):
    """
    View for initiating a request to change the user's password.

    Attributes:
        serializer_class: The serializer class for handling the input data.
        queryset: The queryset of User objects (not used in this view).
        http_method_names: The allowed HTTP methods (POST and GET).
        permission_classes: The permission classes (AllowAny).

    Methods:
        create: Creates a one-time token for password change, stores it in cache, and sends it to the user.

    Raises:
        None
    """
    serializer_class = identity_serializers.ChangePasswordRequestSerializer
    queryset = User.objects.all()
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def perform_create(self, serializer):
        context = self.get_serializer_context()
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.get(username=username)

        cashed_token = custom_classes.CacheManager().set_cache_token(user)
        print(str(cashed_token))

        return super().perform_create(serializer)

    def post(self, request, *args, **kwargs):
        """
        Creates a one-time token for password change, stores it in cache, and sends it to the user.

        Args:
            request: The HTTP request object.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response with a success message and the one-time token.

        Raises:
            None
        """
        cached_token = getattr(self.serializer_class, 'cached_token', None)
        return Response(
            {'message': 'توکن یکبار مصرف برای تغییر رمز ارسال شد.',
             'change_password_token': str(cached_token)},
            status=status.HTTP_200_OK
        )


class ChangePasswordActionView(generics.CreateAPIView):
    """
    View for changing the user's password based on a provided token.

    Attributes:
        serializer_class: The serializer class for handling the input data.
        queryset: The queryset of User objects (not used in this view).
        http_method_names: The allowed HTTP methods (POST and GET).
        permission_classes: The permission classes (AllowAny).

    Methods:
        create: Changes the user's password based on the provided token.

    Raises:
        None
    """
    serializer_class = identity_serializers.ChangePasswordActionSerializer
    queryset = User.objects.all()
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def perform_create(self, request, *args, **kwargs):
        """
        Changes the user's password based on the provided token.

        Args:
            request: The HTTP request object.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response with a success message.

        Raises:
            None
        """
        serializer = self.get_serializer_context()
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {'message': 'رمز عبور با موفقیت تغییر یافت.'},
            status=status.HTTP_200_OK
        )

# It Manger Views


class ItTeacherListCreateView(generics.ListCreateAPIView):
    serializer_class = identity_serializers.ItTeacherListCreateSerializer
    queryset = User.objects.all()
    http_method_names = ['post', 'get']
    permission_classes = (IsAuthenticated, custom_permissions.IsItManager)
