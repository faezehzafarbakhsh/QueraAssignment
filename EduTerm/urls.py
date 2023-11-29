from django.urls import path
from EduTerm import views as edu_term_views
urlpatterns = [
    path('admin/term/', edu_term_views.TermListCreateView.as_view(), name='term_list_create_view'),
    path('admin/term/<int:pk>/', edu_term_views.TermRetrieveUpdateDestroyView.as_view(), name='term_retrieve_update_destroy_view'),
    path('admin/course/term/', edu_term_views.CoursetermFieldListCreateView.as_view(), name='course_term_list_create_view'),
    path('admin/course/term/<int:pk>/', edu_term_views.CoursetermRetrieveUpdateDestroyView.as_view(), name='course_term_retrieve_update_destroy_view'),
]
