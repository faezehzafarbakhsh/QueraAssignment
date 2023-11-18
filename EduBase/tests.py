from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from EduBase import models


class EduFieldListCreateViewTest(APITestCase):
    def setUp(self):
        self.edu_field_url = reverse('edu_field_list_create_view')

        # Sample data for creating an educational field
        self.edu_field_data = {
            'name': 'Computer Science',
            'edu_group': 'Science',
            'unit_count': 4,
            'edu_grade': models.EduField.EduGradeChoices.Undergraduate,
        }

    def test_create_edu_field(self):
        # Test creating an educational field
        response = self.client.post(
            self.edu_field_url, data=self.edu_field_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the educational field is created in the database
        edu_field_exists = models.EduField.objects.filter(
            name=self.edu_field_data['name']).exists()
        self.assertTrue(edu_field_exists)

    def test_list_edu_fields(self):
        # Test listing educational fields
        response = self.client.get(self.edu_field_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_create_edu_field(self):
        # Test creating an educational field with invalid data
        invalid_edu_field_data = {
            'name': '',  # Empty name, which should be invalid
            'edu_group': 'Science',
            'unit_count': 4,
            'edu_grade': models.EduField.EduGradeChoices.Undergraduate,
        }

        response = self.client.post(
            self.edu_field_url, data=invalid_edu_field_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the educational field is not created in the database
        edu_field_exists = models.EduField.objects.filter(
            name=invalid_edu_field_data['name']).exists()
        self.assertFalse(edu_field_exists)
