from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from EduTerm.models import Term, CourseTerm

class TermListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_get_terms(self):
        response = self.client.get('/admin/term/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_term(self):
        data = {'name': 'Test Term'}
        response = self.client.post('/admin/term/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TermRetrieveUpdateDestroyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.term = Term.objects.create(name='Test Term')
        self.client.force_authenticate(user=self.user)

    def test_get_term(self):
        response = self.client.get(f'/admin/term/{self.term.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_term(self):
        data = {'name': 'Updated Term'}
        response = self.client.put(f'/admin/term/{self.term.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Term.objects.get(id=self.term.id).name, 'Updated Term')

    def test_delete_term(self):
        response = self.client.delete(f'/admin/term/{self.term.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    class CoursetermFieldListCreateViewTest(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
            self.client.force_authenticate(user=self.user)

    def test_get_course_terms(self):
        response = self.client.get('/admin/course_term/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_term(self):
        data = {'name': 'Test Course Term'}
        response = self.client.post('/admin/course_term/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(Term.objects.filter(id=self.term.id).exists())



class CoursetermRetrieveUpdateDestroyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.course_term = CourseTerm.objects.create(name='Test Course Term')
        self.client.force_authenticate(user=self.user)

    def test_get_course_term(self):
        response = self.client.get(f'/admin/course_term/{self.course_term.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course_term(self):
        data = {'name': 'Updated Course Term'}
        response = self.client.put(f'/admin/course_term/{self.course_term.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CourseTerm.objects.get(id=self.course_term.id).name, 'Updated Course Term')

    def test_delete_course_term(self):
        response = self.client.delete(f'/admin/course_term/{self.course_term.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CourseTerm.objects.filter(id=self.course_term.id).exists())
