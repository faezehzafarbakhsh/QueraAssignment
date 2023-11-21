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
        self.detail_url = reverse('edu_field_retrieve_update_destroy_view', args=[
            self.edu_field.id])

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


# course
# class CourseTests(APITestCase):
#     def setUp(self):
#         self.college = models.College.objects.create(name='Sample College')
#         self.course_data = {
#             'name': 'Sample Course',
#             'college': self.college,
#             'unit_count': 3,
#             'course_type': 1,
#         }
#         self.course = models.Course.objects.create(**self.course_data)
#         self.course_list_create_url = reverse('course_list_create_view')
#         self.course_detail_url = reverse('course_retrieve_update_destroy_view', args=[self.course.id])
#
#     def test_create_course(self):
#         response = self.client.post(self.course_list_create_url, self.course_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(models.Course.objects.count(), 2)
#
#     def test_get_course_list(self):
#         response = self.client.get(self.course_list_create_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'], 1)
#
#     def test_get_course_detail(self):
#         response = self.client.get(self.course_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], self.course_data['name'])
#
#     def test_update_course(self):
#         college = models.College.objects.create(name='Sample College')
#         updated_data = {
#             'name': 'Updated Course Name',
#             'college': college,
#             'unit_count': 4,
#             'course_type': 2,
#         }
#         response = self.client.put(self.course_detail_url, updated_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.course.refresh_from_db()
#         self.assertEqual(self.course.name, updated_data['name'])
#
#     def test_delete_course(self):
#         response = self.client.delete(self.course_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(models.Course.objects.count(), 0)

# class CourseTests(APITestCase):
#     def setUp(self):
#         self.college = models.College.objects.create(name='Sample College')
#         self.course_data = {
#             'name': 'Sample Course',
#             'college': self.college,  # Pass the College instance directly
#             'unit_count': 3,
#             'course_type': 1,
#         }
#         self.course = models.Course.objects.create(**self.course_data)
#         self.course_list_create_url = reverse('course_list_create_view')
#         self.course_detail_url = reverse('course_retrieve_update_destroy_view', args=[self.course.id])

    # ... rest of your test methods ...

# Course_relation
# class CourseRelationTests(APITestCase):
#     def setUp(self):
#         self.primary_course = models.Course.objects.create(
#             name='Primary Course',
#             college=models.College.objects.create(name='Sample College'),
#             unit_count=3,
#             course_type=1
#         )
#         self.secondary_course = models.Course.objects.create(
#             name='Secondary Course',
#             college=models.College.objects.create(name='Another College'),
#             unit_count=3,
#             course_type=2
#         )
#         self.course_relation_data = {
#             'primary_course': self.primary_course.id,
#             'secondary_course': self.secondary_course.id,
#             'relation_type': 1
#         }
#         self.course_relation = models.CourseRelation.objects.create(**self.course_relation_data)
#         self.course_relation_list_create_url = reverse('course_relation_list_create_view')
#         self.course_relation_detail_url = reverse('course_relation_retrieve_update_destroy_view', args=[self.course_relation.id])
#
#     def test_create_course_relation(self):
#         response = self.client.post(self.course_relation_list_create_url, self.course_relation_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(models.CourseRelation.objects.count(), 2)
#
#     def test_get_course_relation_list(self):
#         response = self.client.get(self.course_relation_list_create_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_get_course_relation_detail(self):
#         response = self.client.get(self.course_relation_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['primary_course'], self.course_relation_data['primary_course'])
#
#     def test_update_course_relation(self):
#         updated_data = {
#             'primary_course': self.primary_course.id,
#             'secondary_course': self.secondary_course.id,
#             'relation_type': 2
#         }
#         response = self.client.put(self.course_relation_detail_url, updated_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.course_relation.refresh_from_db()
#         self.assertEqual(self.course_relation.relation_type, updated_data['relation_type'])
#
#     def test_delete_course_relation(self):
#         response = self.client.delete(self.course_relation_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(models.CourseRelation.objects.count(), 0)
#
# # college
# class CollegeTests(APITestCase):
#     def setUp(self):
#         self.college_data = {
#             'name': 'Sample College',
#         }
#         self.college = models.College.objects.create(**self.college_data)
#         self.college_list_create_url = reverse('college_list_create_view')
#         self.college_detail_url = reverse('college_retrieve_update_destroy_view', args=[self.college.id])
#
#     def test_create_college(self):
#         response = self.client.post(self.college_list_create_url, self.college_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(models.College.objects.count(), 2)
#
#     def test_get_college_list(self):
#         response = self.client.get(self.college_list_create_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_get_college_detail(self):
#         response = self.client.get(self.college_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], self.college_data['name'])
#
#     def test_update_college(self):
#         updated_data = {
#             'name': 'Updated College Name',
#         }
#         response = self.client.put(self.college_detail_url, updated_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.college.refresh_from_db()
#         self.assertEqual(self.college.name, updated_data['name'])
#
#     def test_delete_college(self):
#         response = self.client.delete(self.college_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(models.College.objects.count(), 0)
