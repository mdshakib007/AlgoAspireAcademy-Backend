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
    CourseDetailsSerializer,
    CourseListSerializer,
    CreateCourseSerializer
)

logger = logging.getLogger(__name__)

user = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

@method_decorator(cache_page(60*60), name='dispatch') # caches for 1 hour
class CourseListAPIView(ListAPIView):
    queryset = Course.objects.filter(
        is_published=True,
        is_deleted=False
    ).select_related('instructor')

    serializer_class = CourseListSerializer 
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=['Course'],
        manual_parameters=[
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description="Enable or disable pagination (true or false)",
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(description='List of courses'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred')
        }
    )
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None 

        return super().get(request, *args, **kwargs)


class CourseDetailsAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True, is_deleted=False)
    serializer_class = CourseDetailsSerializer

    @swagger_auto_schema(
        tags=['Course'],
        responses={
            status.HTTP_200_OK: openapi.Response(description='Course details'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Course not found')
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            course = self.get_object()
            serializer = self.get_serializer(course)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self):
        course_id = self.kwargs.get('pk')
        cache_key = f"course_{course_id}"
        course = cache.get(cache_key)

        if not course:
            try:
                course =  Course.objects.filter(
                    is_published=True, 
                    is_deleted=False
                ).prefetch_related('modules').get(pk=course_id)
                cache.set(cache_key, course, timeout=60*10) # cache for 10 minutes
            except Course.DoesNotExist:
                raise NotFound("Course not found")
        
        return course


class CreateCourseAPIView(CreateAPIView):
    serializer_class = CreateCourseSerializer

    @swagger_auto_schema(
        tags=['Course'],
        request_body= CreateCourseSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Course created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_403_FORBIDDEN: openapi.Response(description='You are not authorized to create a course')
        }
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_instructor:
            return super().post(request, *args, **kwargs)
        return Response({'error': 'You are not authorized to create a course'}, status=status.HTTP_403_FORBIDDEN)


class UpdateCourseAPIView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = CreateCourseSerializer
    queryset = Course.objects.filter(is_deleted=False)

    def get_object(self):
        return Course.objects.get(instructor=self.request.user, pk=self.kwargs.get('pk'), is_deleted=False)

    @swagger_auto_schema(
        tags=['Course'],
        request_body= CreateCourseSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Course updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Course not found')
        }
    )
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteCourseAPIView(DestroyAPIView):
    serializer_class = CreateCourseSerializer
    queryset = Course.objects.filter(is_deleted=False)

    def get_object(self):
        return Course.objects.get(instructor=self.request.user, pk=self.kwargs.get('pk'), is_deleted=False)

    @swagger_auto_schema(
        tags=['Course'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Course deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Course not found'),
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.is_published = False 
            instance.save()
            return Response({'success': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
