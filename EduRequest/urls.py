from django.urls import path
from EduRequest import views as edu_request_views

urlpatterns = [
    # Enrollment
    path('admin/enrollment_certificate/' , edu_request_views.EnrollmentCertificateListCreateView.as_view() , name='enrollment_certificate_list_create_view'),
    path('admin/enrollment_certificate/<int:pk>/' , edu_request_views.EnrollmentCertificateRetrieveUpdateDestroyView.as_view() , name='enrollment_certificate_retrieve_update_destroy_view'),
    
    # Student Request
    path('student/me/course_term/<int:course_term_pk>/<int:request_type>/request/',
        edu_request_views.StudentRequestListCreateView.as_view(),
        name='student_request_list_create_view'),
    
    path('student/<int:pk>/course_term/<int:course_term_pk>/<int:request_type>/request/',
        edu_request_views.StudentRequestListCreateView.as_view(),
        name='student_request_list_create_view'),
    
    path('student/me/course_term/<int:course_term_pk>/<int:request_type>/request/<int:pk>/',
        edu_request_views.StudentRequestDetailUpdateDestroyView.as_view(),
        name='student_request_detail_update_destroy_view'),
    
    # Teacher Request
    path('professor/me/course_term',
         edu_request_views.ChancellorRequestListView.as_view(),
         name='professor_request_list_view'),
]
