from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from Identity import models as identity_models

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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_token_login_invalid_token(self):
        data = {'token': 'invalid_token'}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ITTeacherAPITestCase(APITestCase):
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
        user = self.create_authenticated_user()
        # Create a test IT teacher
        self.it_teacher_data = {
            'username': 'it_teacher',
            'email': 'it_teacher@example.com',
            'gender': 1,
            'mobile': '1234567890',
            'national_code': '123456789',
            'expert': 'Programming',
            'level': 'Advanced'
        }
        self.client.force_authenticate(user=user)

    def test_create_it_teacher(self):
        # Replace with your actual URL name
        url = reverse('it-teacher-list-create')
        response = self.client.post(
            url, data=self.it_teacher_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='it_teacher').exists())
        self.assertTrue(identity_models.Teacher.objects.filter(
            expert='Programming', level='Advanced').exists())

    def test_get_it_teacher_list(self):
        # Replace with your actual URL name
        url = reverse('it-teacher-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'],
                         User.objects.filter(is_teacher=True).count())

    def test_get_it_teacher_detail(self):
        it_teacher = User.objects.create_user(
            username='teacher', password='testpassword', is_teacher=True)
        it_teacher.teachers = identity_models.Teacher.objects.create(
            user=it_teacher, expert='Networking', level='Intermediate'
        )

        # Replace with your actual URL name
        url = reverse('it-teacher-detail', kwargs={'pk': it_teacher.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'teacher')
        self.assertEqual(response.data['expert'], 'Networking')
        self.assertEqual(response.data['level'], 'Intermediate')

    def test_update_it_teacher(self):
        it_teacher = User.objects.create_user(
            username='teacher', password='testpassword', is_teacher=True)
        it_teacher.teachers = identity_models.Teacher.objects.create(
            user=it_teacher, expert='Networking', level='Intermediate'
        )

        updated_data = {
            'username': 'aldfjjasdfieh',
            'email': 'newemail@example.com',
            'expert': 'Database',
            'level': 'Beginner',
            'national_code': '12345',
        }

        # Replace with your actual URL name
        url = reverse('it-teacher-detail', kwargs={'pk': it_teacher.id})
        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        it_teacher.refresh_from_db()
        self.assertEqual(it_teacher.email, 'newemail@example.com')
        self.assertEqual(it_teacher.teachers.expert, 'Database')
        self.assertEqual(it_teacher.teachers.level, 'Beginner')

    def test_delete_it_teacher(self):
        it_teacher = User.objects.create_user(
            username='teacher', password='testpassword', is_teacher=True)
        it_teacher.teachers = identity_models.Teacher.objects.create(
            user=it_teacher, expert='Networking', level='Intermediate'
        )

        # Replace with your actual URL name
        url = reverse('it-teacher-detail', kwargs={'pk': it_teacher.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='teacher').exists())
        self.assertFalse(identity_models.Teacher.objects.filter(
            user=it_teacher, expert='Networking', level='Intermediate').exists())


class ITStudentAPITestCase(APITestCase):
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
        user = self.create_authenticated_user()
        # Create a test IT teacher
        self.it_student_data = {
            "username": "student",
            "gender": 1,
            "college": 1,
            "national_code": "54874",
            "entry_year": "2023-11-17",
            "entry_term": 1,
            "average": 2.0,
            "academic_year": 1

        }
        self.client.force_authenticate(user=user)

    def test_create_it_student(self):
        # Replace with your actual URL name
        url = reverse('it-student-list-create')
        response = self.client.post(
            url, data=self.it_student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='student').exists())
        self.assertTrue(identity_models.Student.objects.filter(
            average=2.0, academic_year=1).exists())

    def test_get_it_student_list(self):
        # Replace with your actual URL name
        url = reverse('it-student-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'],
                         User.objects.filter(is_student=True).count())

    def test_get_it_student_detail(self):
        it_student = User.objects.create_user(
            username='student', password='testpassword', is_student=True)
        it_student.students = identity_models.Student.objects.create(
            user=it_student,average=20, academic_year=3
        )

        # Replace with your actual URL name
        url = reverse('it-student-detail', kwargs={'pk': it_student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'student')
        self.assertEqual(response.data['average'], 20)
        self.assertEqual(response.data['academic_year'], 3)

    def test_update_it_student(self):
        it_student = User.objects.create_user(
            username='student', password='testpassword', is_student=True)
        it_student.students = identity_models.Student.objects.create(
            user=it_student,average=20, academic_year=3
        )

        updated_data = {
            'username': 'aldfjjasdfieh',
            'email': 'newemail@example.com',
            "entry_year": "2022-11-17",
            "entry_term": 2,
            "average": 20,
            "academic_year": 3
        }

        # Replace with your actual URL name
        url = reverse('it-student-detail', kwargs={'pk': it_student.id})
        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        it_student.refresh_from_db()
        self.assertEqual(it_student.email, 'newemail@example.com')
        self.assertEqual(it_student.students.entry_year, "2022-11-17")
        self.assertEqual(it_student.students.average, 20)

    def test_delete_it_student(self):
        it_student = User.objects.create_user(
            username='student', password='testpassword', is_student=True)
        it_student.students = identity_models.Student.objects.create(
            user=it_student,average=20, academic_year=3
        )
        # Replace with your actual URL name
        url = reverse('it-student-detail', kwargs={'pk': it_student.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='student').exists())
        self.assertFalse(identity_models.Student.objects.filter(
            user=it_student, expert='Networking', level='Intermediate').exists())
