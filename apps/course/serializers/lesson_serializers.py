from rest_framework import serializers

from apps.course.models import Module, Lesson
from .quiz_serializers import QuizDetailsSerializer
from .assignment_serializers import AssignmentDetailsSerializer


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'module', 'title', 'summary', 
            'lecture_type', 'video', 'text_editorial'
        ]


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'id', 'module', 'title', 'lecture_type'
        ]


class LessonDetailsSerializer(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()
    assignment = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'title', 'summary', 'lecture_type', 
            'video', 'text_editorial', 'quiz', 'assignment'
        ]
    
    def get_quiz(self, obj):
        try:
            return QuizDetailsSerializer(obj.quiz).data
        except Quiz.DoesNotExist:
            return None

    def get_assignment(self, obj):
        try:
            return AssignmentDetailsSerializer(obj.assignment).data
        except Assignment.DoesNotExist:
            return None