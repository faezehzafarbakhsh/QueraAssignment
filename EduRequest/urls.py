from django.urls import path
from EduRequest import views as edu_request_views

urlpatterns = [
    # path('admin/student_request/' , edu_request_views.StudentRequestListCreateView.as_view() , name='student_request_list_create_view'),
    # path('admin/student_request/<int:pk>/', edu_request_views.StudentRequestRetrieveUpdateDestroyView.as_view() , name='student_request_retrieve_update_destroy_view'), 
    path('admin/enrollment_certificate/' , edu_request_views.EnrollmentCertificateListCreateView.as_view() , name='enrollment_certificate_list_create_view'),
    path('admin/enrollment_certificate/<int:pk>/' , edu_request_views.EnrollmentCertificateRetrieveUpdateDestroyView.as_view() , name='enrollment_certificate_retrieve_update_destroy_view'),
    path('student/me/course_term/<int:course_term_pk>/appeal_request/', edu_request_views.AppealAgainstCourseCreateView.as_view(), name='appel_against_course_create_view'),
    path('student/<int:pk>/course_term/<int:course_term_pk>/appeal_request/', edu_request_views.AppealAgainstCourseListCreateView.as_view(), name='appel_against_course_list_create_view'),
    path('student/me/course_term/<int:course_term_pk>/remove-term/', edu_request_views.Delete_Student_SemesterCreateView.as_view(), name='appel_against_course_list_create_view'),
    path('student/<int:pk>/course_term/<int:course_term_pk>/remove-term/', edu_request_views.Delete_Student_SemesterListCreateView.as_view(), name='appel_against_course_list_create_view'),
    path('student/me/course_term/<int:course_term_pk>/emergency-remove/', edu_request_views.Delete_Student_SemesterListCreateView.as_view(), name='appel_against_course_list_create_view'),
    path('student/<int:pk>/course_term/<int:course_term_pk>/emergency-remove/', edu_request_views.Delete_Student_SemesterListCreateView.as_view(), name='appel_against_course_list_create_view'),
    path('admin/appeal_request/<int:pk>/',edu_request_views.AppealAgainstCoursePutView.as_view(),),
    path('admin/appeal_request/',edu_request_views.AppealAgainstCourseListView.as_view(),),
]
