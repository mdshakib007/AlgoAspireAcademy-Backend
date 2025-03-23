from rest_framework import serializers

from apps.course.models import Question


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'quiz', 'title', 'option_a', 'option_b',
            'option_c', 'option_d', 'correct_option',
            'explanation', 'is_published'
        ]


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'title', 'is_published'
        ]


class QuestionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'title', 'option_a', 'option_b',
            'option_c', 'option_d', 'correct_option', 
            'explanation', 'is_published',
            'created_at', 'updated_at'
        ]
