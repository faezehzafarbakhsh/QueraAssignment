from rest_framework import serializers

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from Identity import models as identity_models
from Identity import variable_names as vn_identity

User = get_user_model()

# Authentication Serializers


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, label="تایید گذر واژه", style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email',
                  'national_code', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def create(self, validated_data):
        password = validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserTokenLoginSerializer(serializers.Serializer):
    """
    Serializer for user login using a JWT token.

    Attributes:
        token (str): The JWT token for user authentication.

    Methods:
        validate: Validates the presence of the token, authenticates the user, and logs them in.

    Raises:
        serializers.ValidationError: If the token is missing, the user is not found, or an exception occurs during authentication.
    """
    token = serializers.CharField()

    def validate(self, data):
        """
        Validates the presence of the token, authenticates the user, and logs them in.

        Args:
            data (dict): The input data containing the token.

        Returns:
            dict: The validated data containing the authenticated user.

        Raises:
            serializers.ValidationError: If the token is missing, the user is not found, or an exception occurs during authentication.
        """
        token = data.get('token')

        if not token:
            raise serializers.ValidationError('توکن را وارد کنید.')

        try:
            user_id = AccessToken(token).payload.get('user_id')
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('کاربر یافت نشد.')
        except Exception as e:
            raise serializers.ValidationError(str(e))

        # Manually check if the user is active and log them in
        if user.is_active:
            login(self.context.get('request'), user)

        data['user'] = user
        return data


class ChangePasswordRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for requesting a change of password.

    Attributes:
        username (str): The username for which the password change is requested.

    Methods:
        validate_username: Validates the existence of the user with the provided username.

    Raises:
        serializers.ValidationError: If the user is not found.
    """
    class Meta:
        model = User
        fields = ["username",]

    def validate_username(self, value):
        """
        Validates the existence of the user with the provided username.

        Args:
            value (str): The username to be validated.

        Returns:
            str: The validated username.

        Raises:
            serializers.ValidationError: If the user is not found.
        """
        user = get_object_or_404(User, username=value)


class ChangePasswordActionSerializer(serializers.Serializer):
    """
    Serializer for changing the user password.

    Attributes:
        token (str): The token used for password change verification.
        new_password (str): The new password to be set.
        confirm_password (str): Confirmation of the new password.

    Methods:
        validate_password1: Validates the password according to Django password validation.
        validate: Validates the token and ensures the new password and confirmation match.
        create: Changes the user's password.

    Raises:
        serializers.ValidationError: If the token is invalid, passwords do not match, or password validation fails.
    """
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_password1(self, new_password):
        """
        Validates the password according to Django password validation.

        Args:
            new_password (str): The password to be validated.

        Returns:
            str: The validated password.

        Raises:
            serializers.ValidationError: If the password does not meet validation criteria.
        """
        try:
            validate_password(new_password)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

        return new_password

    def validate(self, data):
        """
        Validates the token and ensures the new password and confirmation match.

        Args:
            data (dict): The input data containing the token and passwords.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the token is invalid or passwords do not match.
        """
        user = self.context['user']
        token = data.get('token')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check if the token is valid
        cache_key = f"change_password_token_{user.id}"
        stored_token = cache.get(cache_key)

        if str(stored_token) != str(token):
            raise serializers.ValidationError("کد نامعتبر است.")

        # Validate new password and confirmation
        if new_password != confirm_password:
            raise serializers.ValidationError("رمز ها مطابقت ندارند.")

        # Additional custom password validation if needed
        # For example, you might want to enforce a certain complexity

        return data

    def create(self, validated_data):
        """
        Changes the user's password.

        Args:
            validated_data (dict): The validated data containing the new password.

        Returns:
            User: The user object with the updated password.
        """
        user = self.context['request'].user

        # Reset the password for the user
        user.password = make_password(validated_data['new_password'])
        user.save()

        # Optionally, you can invalidate the token after it's used
        # cache_key = f"change_password_token_{user.id}"
        # cache.delete(cache_key)

        return user

# It Manager Serializers


class ItTeacherListCreateSerializer(serializers.ModelSerializer):
    expert = serializers.CharField(
        source='teachers.expert', label=vn_identity.TEACHER_EXPERT, max_length=64, )
    level = serializers.CharField(
        source='teachers.level', label=vn_identity.TEACHER_LEVEL, max_length=64, )

    class Meta:
        model = identity_models.User
        fields = ['username', 'password', 'email', 'gender',
                  'mobile', 'national_code', 'expert', 'level']

    def create(self, validated_data):
        teachers_data = validated_data.pop('teachers', {})
        expert = teachers_data.get('expert')
        level = teachers_data.get('level')

        validated_data['is_teacher'] = True

        user_instance = User.objects.create_user(**validated_data)

        identity_models.Teacher.objects.create(
            user=user_instance,
            expert=expert,
            level=level
        )

        return user_instance
