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
    Module, Lesson, Quiz,
    Question, Assignment,
)
from apps.course.serializers import (
    ModuleListSerializer,
    ModuleCreateSerializer,
    ModuleDetailSerializer,
)

logger = logging.getLogger(__name__)

user = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

@method_decorator(cache_page(60*60), name='dispatch')
class ModuleListAPIView(ListAPIView):
    queryset = Module.objects.filter(
        is_published=True, 
        is_deleted= False,
    )

    serializer_class = ModuleListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Module.objects.filter(is_deleted=False)

        course_id = self.request.query_params.get('course_id')

        if course_id:
            queryset = queryset.filter(course=course_id)

        return queryset

    @swagger_auto_schema(
        tags=['Module'],
        manual_parameters=[
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description='Enable or disable pagination (true, false)',
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True,
            ),
            openapi.Parameter(
                'course_id',
                openapi.IN_QUERY,
                description='Filter module by course id',
                type=openapi.TYPE_INTEGER,
                required=False,
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(description='List of modules'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred')
        }
    )
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
        
        return super().get(request, *args, **kwargs)


class ModuleDetailsAPIView(RetrieveAPIView):
    queryset = Module.objects.filter(is_published=True, is_deleted=False)
    serializer_class = ModuleDetailSerializer

    @swagger_auto_schema(
        tags=['Module'],
        responses={
            status.HTTP_200_OK: openapi.Response(description='Module details'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Module not found')
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            module = self.get_object()
            serializer = self.get_serializer(module)
            return Response(serializer.data)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self):
        module_id = self.kwargs.get('pk')
        cache_key = f"module_{module_id}"
        module = cache.get(cache_key)

        if not module:
            try:
                module =  Module.objects.filter(
                    is_published=True, 
                    is_deleted=False
                ).prefetch_related('lessons').get(pk=module_id)
                cache.set(cache_key, module, timeout=60*10) # cache for 10 minutes
            except Module.DoesNotExist:
                raise NotFound("Module not found")
        
        return module


class CreateModuleAPIView(CreateAPIView):
    serializer_class = ModuleCreateSerializer

    @swagger_auto_schema(
        tags=['Module'],
        request_body= ModuleCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Module created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_403_FORBIDDEN: openapi.Response(description='You are not authorized to create a module')
        }
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_instructor:
            return super().post(request, *args, **kwargs)
        return Response({'error': 'You are not authorized to create a module'}, status=status.HTTP_403_FORBIDDEN)


class UpdateModuleAPIView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = ModuleCreateSerializer
    queryset = Module.objects.filter(is_deleted=False)

    def get_object(self):
        return Module.objects.get(course__instructor=self.request.user, pk=self.kwargs.get('pk'), is_deleted=False)

    @swagger_auto_schema(
        tags=['Module'],
        request_body= ModuleCreateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Module updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Module not found')
        }
    )
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteModuleAPIView(DestroyAPIView):
    serializer_class = ModuleCreateSerializer
    queryset = Module.objects.filter(is_deleted=False)

    def get_object(self):
        return Module.objects.get(instructor=self.request.user, pk=self.kwargs.get('pk'), is_deleted=False)

    @swagger_auto_schema(
        tags=['Module'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Module deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Module not found'),
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
            return Response({'success': 'Module deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)
