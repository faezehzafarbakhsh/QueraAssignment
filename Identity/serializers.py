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
from Identity import custom_classes

User = get_user_model()

# Authentication Serializers


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Attributes:
        password2 (str): The confirmation of the user's password.

    Methods:
        create: Creates a new user instance with the provided data.

    Raises:
        serializers.ValidationError: If the passwords do not match.
    """
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
        """
        Creates a new user instance with the provided data.

        Args:
            validated_data (dict): The validated data containing user information.

        Returns:
            User: The newly created user instance.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
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

    Notes:
        This serializer is designed to handle user login using a JWT token. It validates the presence of the token,
        authenticates the user, and logs them in if they are active. If any issues occur during this process,
        a `serializers.ValidationError` is raised with relevant error messages.
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


class UserTokenLoginSerializer(serializers.Serializer):
    """
    Serializer for user login using a JWT token.

    Attributes:
        token (str): The JWT token for user authentication.

    Methods:
        validate: Validates the presence of the token, authenticates the user, and logs them in.

    Raises:
        serializers.ValidationError: If the token is missing, the user is not found, or an exception occurs during authentication.

    Notes:
        This serializer is designed to handle user login using a JWT token. It validates the presence of the token,
        authenticates the user, and logs them in if they are active. If any issues occur during this process,
        a `serializers.ValidationError` is raised with relevant error messages.

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


class ChangePasswordRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a change of password.

    Attributes:
        username (str): The username for which the password change is requested.

    Raises:
        serializers.ValidationError: If the user is not found.
    """
    username = serializers.CharField(max_length=20, label="نام کاربری")

    def validate(self, data):
        """
        Validates the existence of the user with the provided username.

        Args:
            data (dict): The input data containing the username.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the user is not found.
        """
        username = data.get('username')
        user = get_object_or_404(User, username=username)
        return data


class ChangePasswordActionSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password.

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

    Notes:
        This serializer is designed for changing the user's password. It includes methods to validate the new password
        according to Django password validation, verify the token for password change, and ensure that the new password
        and confirmation match. The `create` method is responsible for updating the user's password in the database.

    """
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

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
        stored_token_for_user = self.context['stored_token_for_user']

        user_input_token = data.get('token')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if str(stored_token_for_user) != str(user_input_token):
            raise serializers.ValidationError("توکن نامعتبر است.")

        # Validate new password and confirmation
        if new_password != confirm_password:
            raise serializers.ValidationError("رمز ها مطابقت ندارند.")

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

        return user

# It Manager Serializers


class ItTeacherListCreateSerializer(serializers.ModelSerializer):
    expert = serializers.CharField(
        source='teachers.expert', label=vn_identity.TEACHER_EXPERT, max_length=64, )
    level = serializers.CharField(
        source='teachers.level', label=vn_identity.TEACHER_LEVEL, max_length=64, )

    class Meta:
        model = identity_models.User
        fields = ['username', 'email', 'gender',
                  'mobile', 'national_code', 'expert', 'level']

    def create(self, validated_data):
        teachers_data = validated_data.pop('teachers', {})
        expert = teachers_data.get('expert')
        level = teachers_data.get('level')

        validated_data['is_teacher'] = True

        validated_data['password'] = custom_classes.GlobalFunction.make_random_password()

        # send password as a email to user
        
        user_instance = User.objects.create_user(**validated_data)

        identity_models.Teacher.objects.create(
            user=user_instance,
            expert=expert,
            level=level
        )

        return user_instance

    def update(self, instance, validated_data):
        teachers_data = validated_data.pop('teachers', {})
        expert = teachers_data.get('expert')
        level = teachers_data.get('level')

        # # Update User fields
        # instance.username = validated_data.get('username', instance.username)
        # instance.password = validated_data.get('password', instance.password)
        # instance.email = validated_data.get('email', instance.email)
        # instance.gender = validated_data.get('gender', instance.gender)
        # instance.mobile = validated_data.get('mobile', instance.mobile)
        # instance.national_code = validated_data.get(
        #     'national_code', instance.national_code)

        # Update Teacher fields
        # instance.teachers.expert = expert
        # instance.teachers.level = level

        # Update User fields
        for field in self.fields.keys():
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        # Update Teacher fields
        for field in ['expert', 'level']:
            setattr(instance.teachers, field, locals()[field])

        instance.save()

        return instance
