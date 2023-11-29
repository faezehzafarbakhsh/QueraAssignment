from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from EduTerm import models as term_models
from EduBase import models as base_models
from . import models as request_models
from django.utils import timezone

User = get_user_model()


class StudentRequestTest(APITestCase):
    def create_authenticated_user(self, permissions=None):
        """
        Helper method to create an authenticated user with specific permissions.
        """
        user = User.objects.create_user(
            username='testuser',
            password='testpassword1234',
            email='testuser@example.com',
            is_it_manager=True,
            is_student=True,
        )
        return user

    def setUp(self):
        user = self.create_authenticated_user()
        # Create a test IT teacher
        self.request_data = {
            'request_description': 'gooooz',
        }
        self.college = base_models.College.objects.create(name='college')
        self.course = base_models.Course.objects.create(
            name='course',
            college_id=self.college.id,
            unit_count=2,
            course_type=2,
        )
        self.term = term_models.Term.objects.create(
            name="t1",
            enrollment_start_datetime=timezone.now(),
            enrollment_end_datetime=timezone.now(),
            class_start_datetime=timezone.now(),
            class_end_datetime=timezone.now(),
            modify_start_datetime=timezone.now(),
            modify_end_datetime=timezone.now(),
            emergency_course_drop_end_datetime=timezone.now(),
            exam_start_date=timezone.now().date(),
            term_end_date=timezone.now().date(),
        )
        self.course_term = term_models.CourseTerm.objects.create(
            course_id=self.course.id,
            term_id=self.term.id,
            class_day=timezone.now().date(),
            class_time=timezone.now(),
            exam_datetime=timezone.now(),
            exam_place="RTEYHT",
            teacher_id=user.id,
            capacity=5

        )
        self.request = request_models.StudentRequest.objects.create(
            student_id=user.id,
            term_id=self.term.id,
            course_term_id=self.course_term.id,
            request_description="this a appeal request",
            status=2,
            request_type=1,
        )
        self.url = reverse('student_request_list_create_view',
                           args=[self.course_term.id, 2])
        self.detail_url = reverse('student_request_detail_update_destroy_view',
                                  args=[self.course_term.id, 2, self.request.id])

        self.client.force_authenticate(user=user)

    def test_create_student_request(self):
        response = self.client.post(
            self.url, data=self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(request_models.StudentRequest.objects.filter(
            request_description='gooooz').exists())

    def test_get_student_request_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'],
                         request_models.StudentRequest.objects.count())

    def test_get_student_request_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['request_description'], 'this a appeal request')

    def test_update_student_request(self):

        updated_data = {
            'request_description': 'afshin'
        }

        response = self.client.put(
            self.detail_url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.request.refresh_from_db()
        self.assertEqual(response.data['request_description'], 'afshin')

    def test_delete_student_request(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(request_models.StudentRequest.objects.filter(
            id=self.request.id).exists())
