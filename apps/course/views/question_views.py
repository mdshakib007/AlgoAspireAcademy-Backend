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
    QuestionCreateSerializer,
    QuestionDetailsSerializer,
    QuestionListSerializer
)

logger = logging.getLogger(__name__)

user = get_user_model()


class QuestionListAPIView(ListAPIView):
    pass


class QuestionDetailsAPIView(RetrieveAPIView):
    pass


class CreateQuestionAPIView(CreateAPIView):
    pass


class UpdateQuestionAPIView(UpdateAPIView):
    pass


class DeleteQuestionAPIView(DestroyAPIView):
    pass