from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken



User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                _("نام کاربری قبلا در سامانه ثبت شده است."))
        return username

    def validate_email(self, email):
        # Assuming you have a validate_email function
        validate_email(email)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                _("ایمیل وارد شده قبلا در سامانه ثبت شده است."))

        return email

    def validate_password1(self, password1):
        try:
            validate_password(password1)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

        return password1

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("پسورد ها مطابقت ندارد"))

        return data

    def save(self):
        # You can create the user instance here and return it
        user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            password=self.validated_data['password1']
        )

        return user


class UserTokenLoginSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
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