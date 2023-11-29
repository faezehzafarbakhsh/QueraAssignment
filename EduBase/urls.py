from django.urls import path
from EduBase import views as edu_base_views

urlpatterns = [
    path('admin/faculties/', edu_base_views.CollegeListCreateView.as_view(), name='college_list_create_view'),
    path('admin/faculties/<int:pk>/', edu_base_views.CollegeRetrieveUpdateDestroyView.as_view(), name='college_retrieve_update_destroy_view'),
    path('admin/edu-field/', edu_base_views.EduFieldListCreateView.as_view(), name='edu_field_list_create_view'),
    path('admin/edu-field/<int:pk>/', edu_base_views.EduFieldRetrieveUpdateDestroyView.as_view(), name='edu_field_retrieve_update_destroy_view'),
    path('admin/subjects/', edu_base_views.CourseListCreateView.as_view(), name='course_list_create_view'),
    path('admin/subjects/<int:pk>/', edu_base_views.CourseRetrieveUpdateDestroyView.as_view(), name='course_retrieve_update_destroy_view'),
    path('admin/course-relation-field/', edu_base_views.CourseRelationListCreateView.as_view(), name='course_relation_list_create_view'),
    path('admin/course-relation-field/<int:pk>/', edu_base_views.CourseRelationRetrieveUpdateDestroyView.as_view(), name='course_relation_retrieve_update_destroy_view'),

]
