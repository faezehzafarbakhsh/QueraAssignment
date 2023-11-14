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

    Attributes:
        serializer_class: The serializer class for handling user registration data.
        queryset: The queryset of User objects (not used in this view).
        http_method_names: The allowed HTTP methods (POST).
        permission_classes: The permission classes (AllowAny).

    Methods:
        create: Validates and processes the user registration data, returning a JSON response with the access token.

    Returns:
        Response: JSON response containing the access token upon successful user registration.

    Raises:
        None
    """
    serializer_class = identity_serializers.RegisterSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Validates and processes the user registration data, returning a JSON response with the access token.

        Args:
            request: The HTTP request object.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response containing the access token upon successful user registration.

        Raises:
            None
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserTokenLoginView(generics.CreateAPIView):
    """
    View for user login using JWT token.

    Attributes:
        serializer_class: The serializer class for handling user login with JWT token.
        queryset: The queryset of User objects (not used in this view).
        http_method_names: The allowed HTTP methods (POST).
        permission_classes: The permission classes (AllowAny).

    Methods:
        get_serializer_context: Retrieves the context for the serializer.
        perform_create: Validates and processes the user login data.
        post: Handles the POST request and returns a JSON response upon successful user login.

    Returns:
        Response: JSON response with a success message upon successful user login.

    Raises:
        None
    """
    serializer_class = identity_serializers.UserTokenLoginSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        """
        Retrieves the context for the serializer.

        Returns:
            dict: The context for the serializer.

        Raises:
            None
        """
        context = super().get_serializer_context()
        return context

    def perform_create(self, serializer):
        """
        Validates and processes the user login data.

        Args:
            serializer: The serializer instance.

        Returns:
            Response: JSON response with a success message upon successful user login.

        Raises:
            None
        """
        context = self.get_serializer_context()
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return super().perform_create(serializer)

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request and returns a JSON response upon successful user login.

        Args:
            request: The HTTP request object.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response with a success message upon successful user login.

        Raises:
            None
        """
        return Response({"message": "کاربر با موفقیت وارد سایت شد."}, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
    View for user logout.

    Attributes:
        queryset: The queryset of User objects (not used in this view).
        permission_classes: The permission classes (IsAuthenticated).

    Methods:
        get: Handles the GET request to log the user out.

    Returns:
        Response: JSON response with a success message upon successful user logout.

    Raises:
        None
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to log the user out.

        Args:
            request: The HTTP request object.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response with a success message upon successful user logout.

        Raises:
            None
        """
        logout(request)
        return Response({'message': 'یوزر با موفقیت از سایت خارج شد.'}, status=status.HTTP_200_OK)


class ChangePasswordRequestView(generics.GenericAPIView):
    """
    View for initiating a request to change the user's password.

    Attributes:
        serializer_class: The serializer class for handling the input data.
        queryset: The queryset of User objects (not used in this view).
        http_method_names: The allowed HTTP methods (POST).
        permission_classes: The permission classes (IsAuthenticated).

    Methods:
        post: Creates a one-time token for password change, stores it in cache, and sends it to the user.

    Raises:
        None
    """
    serializer_class = identity_serializers.ChangePasswordRequestSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = (IsAuthenticated,)

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        user = User.objects.get(username=username)

        cached_token = custom_classes.CacheManager().set_cache_token(user)

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
        perform_create: Changes the user's password based on the provided token.

    Raises:
        None
    """
    serializer_class = identity_serializers.ChangePasswordActionSerializer
    queryset = User.objects.all()
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        extra_context = {
            "stored_token_for_user": custom_classes.CacheManager.get_cache_token(user)
        }
        context.update(extra_context)
        return context

    def perform_create(self, serializer):
        """
        Changes the user's password based on the provided token.

        Args:
            serializer: The serializer instance.

        Returns:
            None
        """
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

    def post(self, request, *args, **kwargs):
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
        serializer = self.get_serializer(data=request.data)
        self.perform_create(serializer)

        custom_classes.CacheManager.delete_cache_token(request.user)

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



class ItTeacherRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = identity_serializers.ItTeacherListCreateSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, custom_permissions.IsItManager)
