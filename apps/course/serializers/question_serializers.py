from rest_framework import serializers

from apps.course.models import Question


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'quiz', 'title', 'option_1', 'option_2',
            'option_3', 'option_4', 'correct_option',
            'explanation',
        ]


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'title'
        ]


class QuestionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'title', 'option_1', 'option_2', 
            'option_3', 'option_4', 'correct_option', 
            'selected_option', 'is_correct', 'is_completed',
            'explanation', 
        ]
