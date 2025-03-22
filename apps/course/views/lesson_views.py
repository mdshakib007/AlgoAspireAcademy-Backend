from django.db.models import Prefetch
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
import logging
from drf_yasg import openapi 
from drf_yasg.utils import swagger_auto_schema 
from rest_framework import status 
from rest_framework.views import APIView, Response
from rest_framework.exceptions import NotFound 
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

from apps.course.models import (
    Course, Module, Lesson, Quiz,
    Question, Assignment,
)
from apps.course.serializers import (
    LessonDetailsSerializer,
    LessonListSerializer,
    LessonCreateSerializer
)

logger = logging.getLogger(__name__)

user = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


@method_decorator(cache_page(60*60), name='dispatch')
class LessonListAPIView(ListAPIView):
    serializer_class = LessonListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Lesson.objects.filter(is_deleted=False)
        module_id = self.request.query_params.get('module_id')
        is_published = self.request.query_params.get('is_published')

        if module_id:
            queryset = queryset.filter(module=module_id)
        if is_published:
            is_published = is_published.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(is_published=is_published)
        return queryset
    
    @swagger_auto_schema(
        tags=['Lesson'],
        manual_parameters=[
            openapi.Parameter(
                'module_id',
                openapi.IN_QUERY,
                description='Filter by module id',
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                'is_published',
                openapi.IN_QUERY,
                description='Filter by published or private',
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True
            ),
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description='Enable or disable pagination',
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
        
        return super().get(request, *args, **kwargs)


class LessonDetailsAPIView(RetrieveAPIView):
    queryset = Lesson.objects.filter(is_deleted=False)
    serializer_class = LessonDetailsSerializer

    @swagger_auto_schema(
        tags=['Lesson'],
        responses={
            status.HTTP_200_OK: openapi.Response(description='Lesson details'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Lesson not found')
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            lesson = self.get_object()
            serializer = self.get_serializer(lesson)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_object(self):
        lesson_id = self.kwargs.get('pk')
        cache_key = f"lesson_{lesson_id}"
        lesson = cache.get(cache_key)

        if not lesson:
            try:
                lesson = self.queryset.select_related('quiz', 'assignment').get(pk=lesson_id)
                cache.set(cache_key, lesson, timeout=60*10)
            except Lesson.DoesNotExist:
                raise NotFound("Lesson not found")
        
        return lesson


class CreateLessonAPIView(CreateAPIView):
    serializer_class = LessonCreateSerializer

    @swagger_auto_schema(
        tags=['Lesson'],
        request_body= LessonCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Lesson created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='You are not authorized to create a lesson')
        }
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_instructor:
            return super().post(request, *args, **kwargs)
        return Response({'error': 'You are not authorized to create a lesson'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateLessonAPIView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = LessonCreateSerializer
    queryset = Lesson.objects.filter(is_deleted=False)

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))
    
    @swagger_auto_schema(
        tags=['Lesson'],
        request_body= LessonCreateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Lesson updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Lesson not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to edit lesson')
        }
    )
    def put(self, request, *args, **kwargs):
        if request.user.is_instructor:
            try:
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except Lesson.DoesNotExist:
                return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteLessonAPIView(DestroyAPIView):
    serializer_class = LessonCreateSerializer
    queryset = Lesson.objects.filter(is_deleted=False)

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Lesson'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Lesson deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Lesson not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to delete lesson')
        }
    )
    def delete(self, request, *args, **kwargs):
        if request.user.is_instructor:
            return self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.is_published = False 
            instance.save()
            return Response({'success': 'Lesson deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)