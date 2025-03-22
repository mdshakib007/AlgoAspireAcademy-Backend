from rest_framework import serializers

from apps.course.models import Question, Quiz
from .question_serializers import QuestionDetailsSerializer


class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title', 'lesson', 'is_published']


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'lesson', 'title', 'is_published', 'is_completed']


class QuizDetailsSerializer(serializers.ModelSerializer):
    questions = QuestionDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'lesson', 
            'questions', 'is_published', 'is_completed',
            'created_at', 'updated_at',
        ]