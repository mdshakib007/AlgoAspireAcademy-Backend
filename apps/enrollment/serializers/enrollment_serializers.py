from rest_framework import serializers
from apps.enrollment.models import Enrollment
from apps.enrollment.serializers import LessonCompletionSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'course', 'enrolled_at',
            'is_completed', 'completed_percentage', 
            'completed_at', 'estimate_completion_date',
            'completed_lesson_count', 'completed_quiz_count',
            'completed_assignment_count', 
        ]
        read_only_fields = [
            'id', 'user', 'enrolled_at', 'is_completed',
            'completed_percentage', 'completed_at',
            'estimate_completion_date', 'completed_lesson_count',
            'completed_quiz_count', 'completed_assignment_count',
        ]


class EnrollmentDetailsSerializer(serializers.ModelSerializer):
    lesson_completions = LessonCompletionSerializer(many=True, read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'course', 'enrolled_at',
            'is_completed', 'completed_percentage', 
            'completed_at', 'estimate_completion_date',
            'completed_lesson_count', 'completed_quiz_count',
            'completed_assignment_count', 'lesson_completions',
        ]
        read_only_fields = [
            'id', 'user', 'enrolled_at', 'is_completed',
            'completed_percentage', 'completed_at',
            'estimate_completion_date', 'completed_lesson_count',
            'completed_quiz_count', 'completed_assignment_count',
            'lesson_completions',
        ]