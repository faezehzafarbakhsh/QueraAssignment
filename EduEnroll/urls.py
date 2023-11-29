from django.urls import path
from EduEnroll import views

urlpatterns = [
    path('student/course-selection/create/',
         views.CreateCourseSelectionView.as_view()),
    path('student/<int:pk>/course-selection/create/',
         views.CreateCourseSelectionView.as_view()),
    path('student/course-selection/', views.DetailCourseSelectionView.as_view()),
    path('student/<int:pk>/course-selection/',
         views.DetailCourseSelectionView.as_view()),

    path('student/<int:pk>/course-selection/check/',
         views.CheckCourseSelectionView.as_view()),
    path('student/course-selection/check/',
         views.CheckCourseSelectionView.as_view()),
]
