from django.urls import path
from Identity import views as identity_views

urlpatterns = [
     # Authentication
     path('users/register/', identity_views.UserRegisterIView.as_view()),
     path('users/login/', identity_views.UserTokenLoginView.as_view()),
     path('users/logout/', identity_views.UserLogoutView.as_view()),
     # Change Password
     path('users/change-password-request/',
          identity_views.ChangePasswordRequestView.as_view()),
     path('users/change-password-action/',
          identity_views.ChangePasswordActionView.as_view()),

     # Users crud
     path('admin/professors/', identity_views.ItTeacherListCreateView.as_view()),
     path('admin/professors/<int:pk>/', identity_views.ItTeacherRetrieveUpdateDestroyView.as_view()),



]
