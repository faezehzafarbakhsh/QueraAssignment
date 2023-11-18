from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from EduBase import models


class EduFieldTests(APITestCase):
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

    def test_create_edu_field(self):
        response = self.client.post(self.edu_field_url, self.edu_field_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming you have one existing object
        self.assertEqual(models.EduField.objects.count(), 2)

    def test_get_edu_field_list(self):
        response = self.client.get(self.edu_field_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming you have one existing object
        self.assertEqual(len(response.data), 1)

    def test_get_edu_field_detail(self):
        detail_url = reverse('edu_field_retrieve_update_destroy_view', args=[
                             self.edu_field.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.edu_field_data['name'])

    def test_update_edu_field(self):
        detail_url = reverse('edu_field_retrieve_update_destroy_view', args=[
                             self.edu_field.id])
        updated_data = {
            'name': 'Updated Field Name',
            'edu_group': 'Updated Group',
            'unit_count': 4,
            'edu_grade': 3,  # Assuming 3 corresponds to 'MastersDegree' in your choices
        }
        response = self.client.put(detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.edu_field.refresh_from_db()
        self.assertEqual(self.edu_field.name, updated_data['name'])

    def test_delete_edu_field(self):
        detail_url = reverse('edu_field_retrieve_update_destroy_view', args=[
                             self.edu_field.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.EduField.objects.count(), 0)
