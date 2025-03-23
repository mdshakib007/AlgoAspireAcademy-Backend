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

from apps.course.models import Assignment
from apps.course.serializers import (
    AssignmentCreateSerializer,
    AssignmentDetailsSerializer,
    AssignmentListSerializer
)

logger = logging.getLogger(__name__)

user = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class AssignmentListAPIView(ListAPIView):
    serializer_class = AssignmentListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Assignment.objects.all()
        lesson_id = self.request.query_params.get('lesson_id')
        is_published = self.request.query_params.get('is_published')

        if lesson_id:
            queryset = queryset.filter(lesson=lesson_id)
        if is_published:
            is_published = is_published.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(is_published=is_published)
        return queryset

    @swagger_auto_schema(
        tags=['Assignment'],
        manual_parameters=[
            openapi.Parameter(
                'lesson_id',
                openapi.IN_QUERY,
                description='Filter by lesson id',
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


class AssignmentDetailsAPIView(RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentDetailsSerializer

    @swagger_auto_schema(
        tags=['Assignment'],
        responses={
            status.HTTP_200_OK: openapi.Response(description='Assignment details'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Assignment not found')
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            assignment = self.get_object()
            serializer = self.get_serializer(assignment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Assignment.DoesNotExist:
            return Response({'error': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_object(self):
        assignment_id = self.kwargs.get('pk')

        try:
            assignment = self.queryset.get(pk=assignment_id)
        except Assignment.DoesNotExist:
            raise NotFound("Assignment not found")
        
        return assignment


class CreateAssignmentAPIView(CreateAPIView):
    serializer_class = AssignmentCreateSerializer

    @swagger_auto_schema(
        tags=['Assignment'],
        request_body= AssignmentCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Assignment created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='You are not authorized to create a assignment')
        }
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_instructor:
            return super().post(request, *args, **kwargs)
        return Response({'error': 'You are not authorized to create a assignment'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateAssignmentAPIView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = AssignmentCreateSerializer
    queryset = Assignment.objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Assignment'],
        request_body= AssignmentCreateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Assignment updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Assignment not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to edit assignment')
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
            except Assignment.DoesNotExist:
                return Response({'error': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteAssignmentAPIView(DestroyAPIView):
    serializer_class = AssignmentCreateSerializer
    queryset = Assignment.objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Assignment'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Assignment deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Assignment not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to delete assignment')
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
            return Response({'success': 'Assignment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Assignment.DoesNotExist:
            return Response({'error': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)