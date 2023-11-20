from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

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
