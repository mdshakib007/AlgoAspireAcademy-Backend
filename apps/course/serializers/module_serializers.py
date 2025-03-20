from rest_framework import serializers

from apps.course.models import Module
from .lesson_serializers import LessonListSerializer


class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'course', 'title', 'summary',
        ]
        

class ModuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'id', 'course', 'title', 'is_completed',
            'completed_lessons_count',
        ]


class ModuleDetailSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            'id', 'course', 'title', 'summary', 'is_completed', 
            'completed_lessons_count', 'lessons'
        ]
