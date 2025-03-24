from django.contrib.auth import get_user_model
import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from apps.enrollment.models import LessonCompletion, Enrollment
from apps.enrollment.serializers import LessonCompletionSerializer

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class LessonCompletionListAPIView(ListAPIView):
    serializer_class = LessonCompletionSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = LessonCompletion.objects.all()
        enrollment_id = self.request.query_params.get('enrollment_id')

        if enrollment_id:
            queryset = queryset.filter(enrollment=
            enrollment_id)
        return queryset

    @swagger_auto_schema(
        tags=['Lesson Completion'],
        manual_parameters=[
            openapi.Parameter(
                'enrollment_id',
                openapi.IN_QUERY,
                description='Filter by enrolled course id',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description='Enable or disable pagination',
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None

        return super().get(request, *args, **kwargs)


class LessonCompletionDetailsAPIView(RetrieveAPIView):
    queryset = LessonCompletion.objects.all()
    serializer_class = LessonCompletionSerializer

    @swagger_auto_schema(
        tags=['Lesson Completion'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Lesson completion details'
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description='You are not authorized to view'
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Not found'
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='An error occurred'
            )
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            lesson_completion = self.get_object()
            serializer = self.get_serializer(lesson_completion)
            return Response(serializer.data, status.HTTP_200_OK)
        except LessonCompletion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get_object(self):
        id = self.kwargs.get('pk')
        
        try:
            lesson_completion = self.queryset.get(pk=id)
        except LessonCompletion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return lesson_completion


class LessonCompletionCreateAPIView(CreateAPIView):
    serializer_class = LessonCompletionSerializer

    @swagger_auto_schema(
        tags=['Lesson Completion'],
        request_body= LessonCompletionSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Lesson completed successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='You are not authorized to complete')
        }
    )
    def post(self, request, *args, **kwargs):
        enrollment_id = request.data.get('enrollment')
        try:
            enrollment = Enrollment.objects.get(pk=enrollment_id)
        except Enrollment.DoesNotExist:
            return Response({'error' : 'enrollment not found'}, status=status.HTTP_404_NOT_FOUND)

        if enrollment.user == request.user:
            return super().post(request, *args, **kwargs)
        return Response({'error': 'You are not authorized to create a lesson'}, status=status.HTTP_401_UNAUTHORIZED)


class LessonCompletionDeleteAPIView(DestroyAPIView):
    serializer_class = LessonCompletionSerializer
    queryset = LessonCompletion.objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Lesson Completion'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Lesson completion deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Lesson completion not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to delete')
        }
    )
    def delete(self, request, *args, **kwargs):
        if request.user.is_instructor:
            return self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({'success': 'Lesson completion deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson completion not found'}, status=status.HTTP_404_NOT_FOUND)