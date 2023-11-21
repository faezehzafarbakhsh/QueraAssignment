from django.urls import path
from Identity import views as identity_views

urlpatterns = [
    # Authentication
    path('users/register/', identity_views.UserRegisterIView.as_view(), name="user_register"),
    path('users/login/', identity_views.UserTokenLoginView.as_view(), name ="user_token_login"),
    path('users/logout/', identity_views.UserLogoutView.as_view()),

    # Change Password
    path('users/change-password-request/',
         identity_views.ChangePasswordRequestView.as_view(), name="change_password_request"),
    path('users/change-password-action/',
         identity_views.ChangePasswordActionView.as_view(), name="change_password_action"),

    # Users crud

    # Teachers
    path('admin/professors/', identity_views.ItTeacherListCreateView.as_view(), name='it-teacher-list-create'),
    path('admin/professors/<int:pk>/',
         identity_views.ItTeacherRetrieveUpdateDestroyView.as_view(),name ='it-teacher-detail'),

    # Students
    path('admin/students/', identity_views.ItStudentListCreateView.as_view(), name='it-student-list-create'),
    path('admin/students/<int:pk>/',
         identity_views.ItStudentRetrieveUpdateDestroyView.as_view(), name='it-student-detail'),

    # Chancellors
    path('admin/assistants/', identity_views.ItChancellorListCreateView.as_view()),
    path('admin/assistants/<int:pk>/',
         identity_views.ItChancellorRetrieveUpdateDestroyView.as_view()),

    path('students/', identity_views.ChancellorStudentsListView.as_view()),
    path('students/<int:pk>/',
         identity_views.ChancellorStudentRetrieveUpdateDestroyView.as_view()),

     # Token
     path('token/', identity_views.CustomTokenObtainPairView.as_view(),)


]
