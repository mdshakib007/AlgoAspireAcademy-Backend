from django.urls import path, include

from apps.course.views import (
    # courses
    CourseListAPIView,
    CourseDetailsAPIView,
    CreateCourseAPIView,
    UpdateCourseAPIView,
    DeleteCourseAPIView,

    # modules
    ModuleListAPIView,

)

urlpatterns = [
    # Course API URLs
    path('list/', CourseListAPIView.as_view(), name='course-list'),
    path('details/<int:pk>/', CourseDetailsAPIView.as_view(), name='course-details'),
    path('create/', CreateCourseAPIView.as_view(), name='create-course'),
    path('update/<int:pk>/', UpdateCourseAPIView.as_view(), name='update-course'),
    path('delete/<int:pk>/', DeleteCourseAPIView.as_view(), name='delete-course'),

    # Module API URLs
    # path('module/list/', ModuleListAPIView.as_view(), name='module-list'),
    # path('module/details/<int:pk>/', ModuleDetailsAPIView.as_view(), name='module-details'),
    # path('module/create/', CreateModuleAPIView.as_view(), name='create-module'),
    # path('module/update/<int:pk>/', UpdateModuleAPIView.as_view(), name='update-module'),
    # path('module/delete/<int:pk>/', DeleteModuleAPIView.as_view(), name='delete-module'),

    # Lesson API URLs
    # path('lesson/list/', LessonListAPIView.as_view(), name='lesson-list'),
    # path('lesson/details/<int:pk>/', LessonDetailsAPIView.as_view(), name='lesson-details'),
    # path('lesson/create/', CreateLessonAPIView.as_view(), name='create-lesson'),
    # path('lesson/update/<int:pk>/', UpdateLessonAPIView.as_view(), name='update-lesson'),
    # path('lesson/delete/<int:pk>/', DeleteLessonAPIView.as_view(), name='delete-lesson'),

    # Quiz API URLs
    # path('quiz/list/', QuizListAPIView.as_view(), name='quiz-list'),
    # path('quiz/details/<int:pk>/', QuizDetailsAPIView.as_view(), name='quiz-details'),
    # path('quiz/create/', CreateQuizAPIView.as_view(), name='create-quiz'),
    # path('quiz/update/<int:pk>/', UpdateQuizAPIView.as_view(), name='update-quiz'),
    # path('quiz/delete/<int:pk>/', DeleteQuizAPIView.as_view(), name='delete-quiz'),

    # Question API URLs
    # path('question/list/', QuestionListAPIView.as_view(), name='question-list'),
    # path('question/details/<int:pk>/', QuestionDetailsAPIView.as_view(), name='question-details'),
    # path('question/create/', CreateQuestionAPIView.as_view(), name='create-question'),
    # path('question/update/<int:pk>/', UpdateQuestionAPIView.as_view(), name='update-question'),
    # path('question/delete/<int:pk>/', DeleteQuestionAPIView.as_view(), name='delete-question'),

    # Assignment API URLs
    # path('assignment/list/', AssignmentListAPIView.as_view(), name='assignment-list'),
    # path('assignment/details/<int:pk>/', AssignmentDetailsAPIView.as_view(), name='assignment-details'),
    # path('assignment/create/', CreateAssignmentAPIView.as_view(), name='create-assignment'),
    # path('assignment/update/<int:pk>/', UpdateAssignmentAPIView.as_view(), name='update-assignment'),
    # path('assignment/delete/<int:pk>/', DeleteAssignmentAPIView.as_view(), name='delete-assignment'),
]
