from django.urls import path
from .views import TeacherListOrCreateView

urlpatterns = [
    path('admin/professors/', TeacherListOrCreateView.as_view(), name='teacher-list-create'),
]