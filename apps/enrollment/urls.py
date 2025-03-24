from django.urls import path
from apps.enrollment.views import (
    EnrollmentCreateAPIView,
    EnrollmentDeleteAPIView,
    EnrollmentDetailsAPIView,
    EnrollmentListAPIView,

    LessonCompletionCreateAPIView,
    LessonCompletionDeleteAPIView,
    LessonCompletionDetailsAPIView,
    LessonCompletionListAPIView,
)


urlpatterns = [
    path('create/', EnrollmentCreateAPIView.as_view(), name='enrollment-create'),
    path('details/<int:pk>/', EnrollmentDetailsAPIView.as_view(), name='enrollment-details'),
    path('list/', EnrollmentListAPIView.as_view(), name='enrollment-list'),
    path('delete<int:pk>/', EnrollmentDeleteAPIView.as_view(), name='enrollment-delete'),
    
    path('complete-lesson/create/', LessonCompletionCreateAPIView.as_view(), name='lesson-complete-create'),
    path('complete-lesson/details/<int:pk>/', LessonCompletionDetailsAPIView.as_view(), name='lesson-complete-details'),
    path('complete-lesson/list/', LessonCompletionListAPIView.as_view(), name='lesson-complete-list'),
    path('complete-lesson/delete/<int:pk>/', LessonCompletionDeleteAPIView.as_view(), name='lesson-complete-delete'),
]
