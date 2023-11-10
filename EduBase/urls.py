from django.urls import path
from EduBase import views as edu_base_views

urlpatterns = [
    path('admin/college/', edu_base_views.CollegeListCreateView.as_view(), name='college_list_create_view'),
    path('admin/college/<int:pk>/', edu_base_views.CollegeRetrieveUpdateDestroyView.as_view(), name='college_retrieve_update_destroy_view'),
    path('admin/edu_field/', edu_base_views.EduFieldListCreateView.as_view(), name='edu_field_list_create_view'),
    path('admin/edu_field/<int:pk>/', edu_base_views.EduFieldRetrieveUpdateDestroyView.as_view(), name='edu_field_retrieve_update_destroy_view'),
]
