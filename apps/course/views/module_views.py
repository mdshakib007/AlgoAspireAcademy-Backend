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
    ModuleListSerializer,
    ModuleCreateSerializer,
    ModuleDetailSerializer,
)

logger = logging.getLogger(__name__)

user = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class ModuleListAPIView(ListAPIView):
    queryset = Module.objects.filter(
        is_published=True, 
        is_deleted= False,
    )

    serializer_class = ModuleListSerializer
    pagination_class = CustomPagination

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
        
        try:
            module = self.get_object()
            serializer = self.get_serializer(module)
            return Response(serializer.data)
        except Module.DoesNotExist:
            return Response({'error':'Module not found'}, status=status.HTTP_404_NOT_FOUND)
        
    # def get_object(self):
    #     course_id = self.kwargs.get('pk')
    #     cache_key