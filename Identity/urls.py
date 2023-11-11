from django.urls import path
from Identity import views as identity_views

urlpatterns = [
    path('auth/register/', identity_views.UserRegisterIView.as_view()),
    path('auth/login/', identity_views.UserTokenLoginView.as_view()),
]
