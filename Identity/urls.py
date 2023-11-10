from django.urls import path
from .views import UserRegisterIView

urlpatterns = [
    path("auth/register/", UserRegisterIView.as_view()),
]
