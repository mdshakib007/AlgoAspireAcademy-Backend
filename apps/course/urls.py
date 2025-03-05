from django.urls import path, include

from apps.course.views import (
    CourseListAPIView,
    CourseDetailsAPIView,
    CreateCourseAPIView,
    UpdateCourseAPIView,
    DeleteCourseAPIView,
)

urlpatterns = [
    # Course API URLs
    path('list/', CourseListAPIView.as_view(), name='course-list'),
    path('details/<int:pk>/', CourseDetailsAPIView.as_view(), name='course-details'),
    path('create/', CreateCourseAPIView.as_view(), name='create-course'),
    path('update/<int:pk>/', UpdateCourseAPIView.as_view(), name='update-course'),
    path('delete/<int:pk>/', DeleteCourseAPIView.as_view(), name='delete-course'),

    # Module API URLs

    # Lesson API URLs

    # Quiz API URLs

    # Assignment API URLs
    
]
