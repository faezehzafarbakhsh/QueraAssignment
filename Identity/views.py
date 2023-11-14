from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken


from Identity import models as identity_models
from Identity import serializers as identity_serializers
from Identity import permisson_classes as custom_permissons

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

    def perform_create(self, serializer):
        """
        Custom method to perform additional actions after user creation.

        Args:
            serializer (RegisterSerializer): The serializer instance.

        Returns:
            Response: JSON response containing the access token and its details.
        """
        access, user = serializer.save()

        return Response({
            "token": access, 
        }, status=status.HTTP_201_CREATED)


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

    def post(self, request, *args, **kwargs):
        """
        Custom method to handle user login.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: JSON response with a success message.
        """
        serializer = self.get_serializer(data=request.data, context={
                                         'view': self, 'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({"message": "کاربر با موفقیت وارد سایت شد."}, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
    View for user logout.

    Args:
        generics (class): Django REST Framework generics class.

    Returns:
        Response: JSON response with a success message upon successful user logout.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Custom method to handle user logout.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: JSON response with a success message.
        """
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


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

    def create(self, request, *args, **kwargs):
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

        # Generate and store the one-time code in cache
        # token = AccessToken.for_user(user)
        # cache_key = f"change_password_token_{user.id}"
        # cache.set(cache_key, token, timeout=3 * 60)

        # You can send the code through an email or any other means here

        return Response(
            {'message': 'توکن یکبار مصرف برای تغییر رمز ارسال شد.',
             'change_password_token': str(token)},
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

    def create(self, request, *args, **kwargs):
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
        serializer = self.get_serializer(
            data=request.data, context={'view': self, 'user': request.user})
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {'message': 'رمز عبور با موفقیت تغییر یافت.'},
            status=status.HTTP_200_OK
        )

# It Manger Views


class ItTeacherListCreateView(generics.ListCreateAPIView):
    serializer_class = identity_serializers.ItTeacherListCreateSerializer
