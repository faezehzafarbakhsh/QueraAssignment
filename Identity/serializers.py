from rest_framework import serializers

from django.core.cache import cache
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.

    Attributes:
        username (str): The desired username for the new user.
        email (str): The email address of the new user.
        password1 (str): The password for the new user.
        password2 (str): Confirmation of the password for the new user.

    Methods:
        validate_username: Validates the uniqueness of the username.
        validate_email: Validates the uniqueness of the email address.
        validate_password1: Validates the password according to Django password validation.
        validate: Validates that password1 and password2 match.
        save: Creates and returns a new user instance.

    Raises:
        serializers.ValidationError: If any validation checks fail.
    """
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, style={
                                      'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={
                                      'input_type': 'password'})

    def validate_username(self, username):
        """
        Validates the uniqueness of the username.

        Args:
            username (str): The username to be validated.

        Returns:
            str: The validated username.

        Raises:
            serializers.ValidationError: If the username is not unique.
        """
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                _("نام کاربری قبلا در سامانه ثبت شده است."))
        return username

    def validate_email(self, email):
        """
        Validates the uniqueness of the email address.

        Args:
            email (str): The email address to be validated.

        Returns:
            str: The validated email address.

        Raises:
            serializers.ValidationError: If the email address is not unique.
        """
        validate_email(email)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                _("ایمیل وارد شده قبلا در سامانه ثبت شده است."))

        return email

    def validate_password1(self, password1):
        """
        Validates the password according to Django password validation.

        Args:
            password1 (str): The password to be validated.

        Returns:
            str: The validated password.

        Raises:
            serializers.ValidationError: If the password does not meet validation criteria.
        """
        try:
            validate_password(password1)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

        return password1

    def validate(self, data):
        """
        Validates that password1 and password2 match.

        Args:
            data (dict): The input data containing password1 and password2.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If password1 and password2 do not match.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("پسورد ها مطابقت ندارد"))

        return data

    def save(self):
        """
        Creates and returns a new user instance.

        Returns:
            tuple: A tuple containing the user instance and the access token.
        """
        user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            password=self.validated_data['password1']
        )
        access = AccessToken.for_user(user)
        print(access)
        return str(access), user


class UserTokenLoginSerializer(serializers.Serializer):
    """
    Serializer for user login using a JWT token.

    Attributes:
        token (str): The JWT token for user authentication.

    Methods:
        validate: Validates the presence of the token and authenticates the user.

    Raises:
        serializers.ValidationError: If the token is missing, the user is not found, or an exception occurs during authentication.
    """
    token = serializers.CharField()

    def validate(self, data):
        """
        Validates the presence of the token and authenticates the user.

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

        user = authenticate(request=self.context.get('request'), user=user)
        data['user'] = user
        return data


class ChangePasswordRequestSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("کاربر یافت نشد.")
        return value


class ChangePasswordActionSerializer(serializers.Serializer):
    code = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_password1(self, new_password):
        """
        Validates the password according to Django password validation.

        Args:
            password1 (str): The password to be validated.

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
        code = data.get('code')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check if the code is valid
        # Access the user_id from the view's kwargs
        user_id = self.context['view'].kwargs.get('pk')
        cache_key = f"change_password_code_{user_id}"
        stored_code = cache.get(cache_key)

        if stored_code is None or stored_code != code:
            raise serializers.ValidationError("کد نامعتبر است.")

        # Validate new password and confirmation
        if new_password != confirm_password:
            raise serializers.ValidationError("رمز ها مطابقت ندارند.")

        # Additional custom password validation if needed
        # For example, you might want to enforce a certain complexity

        return data

    def create(self, validated_data):
        user_id = self.context['view'].kwargs.get('pk')
        user = User.objects.get(id=user_id)

        # Reset the password for the user
        user.password = set_password(validated_data['new_password'])
        user.save()

        # Optionally, you can invalidate the code after it's used
        cache_key = f"change_password_code_{user_id}"
        cache.delete(cache_key)

        return user
