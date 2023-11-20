from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class UserRegisterIViewTest(APITestCase):
    def test_user_registration(self):
        """
        Test user registration.
        """
        url = reverse("user_register")

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'national_code': '1234567890',
            'password': 'testpassword',
            'password2': 'testpassword',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the user was created in the database
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.national_code, '1234567890')

        # Add more assertions as needed

        # Verify that the password is not stored in plain text
        self.assertNotEqual(user.password, 'testpassword')

        # Verify that the password can be used to authenticate the user
        self.assertTrue(user.check_password('testpassword'))


class UserTokenLoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@example.com')
        self.token = AccessToken.for_user(self.user)
        self.url = reverse('user_token_login')

    def test_user_token_login_success(self):
        data = {'token': str(self.token)}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'کاربر با موفقیت وارد سایت شد.')

    def test_user_token_login_missing_token(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_token_login_invalid_token(self):
        data = {'token': 'invalid_token'}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ChangePasswordRequestViewTest(APITestCase):
    def test_successful_request(self):
        url = reverse('change_password_request')  # Change this to your actual URL name
        data = {'username': 'testuser'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('change_password_token', response.data)

class ChangePasswordActionViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = self.client.post(reverse('token_obtain_pair'),self.user)

    def test_successful_password_change(self):
        url = reverse('change_password_action')  # Change this to your actual URL name
        data = {
            'token': self.token,
            'new_password': 'new_password123',
            'confirm_password': 'new_password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'رمز عبور با موفقیت تغییر یافت.')

    def test_invalid_token(self):
        url = reverse('change-password-action')  # Change this to your actual URL name
        data = {
            'token': 'invalid_token',
            'new_password': 'new_password123',
            'confirm_password': 'new_password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('توکن نامعتبر است.', response.data['non_field_errors'])

    def test_passwords_do_not_match(self):
        url = reverse('change-password-action')  # Change this to your actual URL name
        data = {
            'token': self.token,
            'new_password': 'new_password123',
            'confirm_password': 'wrong_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('رمز ها مطابقت ندارند.', response.data['non_field_errors'])

    def tearDown(self):
        cache.clear() 