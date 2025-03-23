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

from apps.course.models import Question
from apps.course.serializers import (
    QuestionCreateSerializer,
    QuestionDetailsSerializer,
    QuestionListSerializer
)

logger = logging.getLogger(__name__)

user = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class QuestionListAPIView(ListAPIView):
    serializer_class = QuestionCreateSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Question.objects.all()
        quiz_id = self.request.query_params.get('quiz_id')
        is_published = self.request.query_params.get('is_published')

        if quiz_id:
            queryset = queryset.filter(quiz=quiz_id)
        if is_published:
            is_published = is_published.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(is_published=is_published)
        return queryset
    
    @swagger_auto_schema(
        tags=['Question'],
        manual_parameters=[
            openapi.Parameter(
                'quiz_id',
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


class QuestionDetailsAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailsSerializer

    @swagger_auto_schema(
        tags=['Question'],
        responses={
            status.HTTP_200_OK: openapi.Response(description='Question details'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Question not found')
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            question = self.get_object()
            serializer = self.get_serializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_object(self):
        question_id = self.kwargs.get('pk')

        try:
            question = self.queryset.get(pk=question_id)
        except Question.DoesNotExist:
            raise NotFound("Question not found")
        
        return question


class CreateQuestionAPIView(CreateAPIView):
    serializer_class = QuestionCreateSerializer

    @swagger_auto_schema(
        tags=['Question'],
        request_body= QuestionCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Question created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='You are not authorized to create a Question')
        }
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_instructor:
            return super().post(request, *args, **kwargs)
        return Response({'error': 'You are not authorized to create a Question'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateQuestionAPIView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = QuestionCreateSerializer
    queryset = Question.objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))
    
    @swagger_auto_schema(
        tags=['Question'],
        request_body= QuestionCreateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Question updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Question not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to edit Question')
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
            except Question.DoesNotExist:
                return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteQuestionAPIView(DestroyAPIView):
    serializer_class = QuestionCreateSerializer
    queryset = Question.objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Question'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Question deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Question not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to delete Question')
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
            return Response({'success': 'Question deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)