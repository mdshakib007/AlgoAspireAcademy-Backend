from rest_framework import serializers

from apps.course.models import Module
from .lesson_serializers import LessonListSerializer


class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'course', 'title', 'summary', 
            'lesson_count', 'is_published',
        ]


class ModuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'id', 'course', 'title',
            'lesson_count', 'is_published'
        ]


class ModuleDetailSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            'id', 'course', 'title', 'summary',
            'lesson_count', 'lessons',
            'is_published', 'created_at', 'updated_at',
        ]
