from rest_framework import serializers

from apps.course.models import Module, Lesson, Quiz, Assignment
from .quiz_serializers import QuizDetailsSerializer
from .assignment_serializers import AssignmentDetailsSerializer
 

class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'module', 'title', 'summary', 
            'lecture_type', 'video', 'text_editorial',
            'is_published',
        ]


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'title', 'lecture_type', 
            'is_published',
        ]


class LessonDetailsSerializer(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()
    assignment = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'title', 'summary', 'lecture_type', 
            'video', 'text_editorial', 'quiz', 'assignment', 
            'is_published', 'created_at', 'updated_at'
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