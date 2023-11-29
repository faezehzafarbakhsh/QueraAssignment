
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from EduBase import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EduFieldTests(APITestCase):
    def create_authenticated_user(self, permissions=None):
        """
        Helper method to create an authenticated user with specific permissions.
        """
        user = User.objects.create_user(
            username='testuser',
            password='testpassword1234',
            email='testuser@example.com',
            is_it_manager=True,
        )
        return user

    def setUp(self):
        # Create some sample data for testing
        self.edu_field_data = {
            'name': 'Sample Field',
            'edu_group': 'Sample Group',
            'unit_count': 3,
            'edu_grade': 2,  # Assuming 2 corresponds to 'Undergraduate' in your choices
        }
        self.edu_field = models.EduField.objects.create(**self.edu_field_data)
        self.edu_field_url = reverse('edu_field_list_create_view')
        self.detail_url = reverse('edu_field_retrieve_update_destroy_view', args=[
            self.edu_field.id])
        self.client.force_authenticate(user=self.create_authenticated_user())

    def test_create_edu_field(self):
        response = self.client.post(self.edu_field_url, self.edu_field_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming you have one existing object
        self.assertEqual(models.EduField.objects.count(), 2)

    def test_get_edu_field_list(self):
        response = self.client.get(self.edu_field_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming you have one existing object
        self.assertEqual(response.data['count'], 1)

    def test_get_edu_field_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.edu_field_data['name'])

    def test_update_edu_field(self):
        updated_data = {
            'name': 'Updated Field Name',
            'edu_group': 'Updated Group',
            'unit_count': 4,
            'edu_grade': 3,  # Assuming 3 corresponds to 'MastersDegree' in your choices
        }
        response = self.client.put(self.detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.edu_field.refresh_from_db()
        self.assertEqual(self.edu_field.name, updated_data['name'])

    def test_delete_edu_field(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.EduField.objects.count(), 0)


class CollegeTests(APITestCase):
    def create_authenticated_user(self, permissions=None):
        """
        Helper method to create an authenticated user with specific permissions.
        """

        user = User.objects.create_user(
            username='testuser',
            password='testpassword1234',
            email='testuser@example.com',
            is_it_manager=True,
        )
        return user

    def setUp(self):
        self.college_data = {
            'name': 'Sample College',
        }
        self.college = models.College.objects.create(**self.college_data)
        self.college_list_create_url = reverse('college_list_create_view')
        self.college_detail_url = reverse(
            'college_retrieve_update_destroy_view', args=[self.college.id])
        self.client.force_authenticate(user=self.create_authenticated_user())

    def test_create_college(self):
        response = self.client.post(
            self.college_list_create_url, self.college_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.College.objects.count(), 2)

    def test_get_college_list(self):
        response = self.client.get(self.college_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_college_detail(self):
        response = self.client.get(self.college_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.college_data['name'])

    def test_update_college(self):
        updated_data = {
            'name': 'Updated College Name',
        }
        response = self.client.put(self.college_detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.college.refresh_from_db()
        self.assertEqual(self.college.name, updated_data['name'])

    def test_delete_college(self):
        response = self.client.delete(self.college_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.College.objects.count(), 0)
