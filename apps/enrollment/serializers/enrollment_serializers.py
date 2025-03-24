from rest_framework import serializers
from apps.enrollment.models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'user', 'course', 'enrolled_at',
            'is_completed', 'completed_percentage', 
            'completed_at', 'estimate_completion_date',
            'completed_lesson_count', 'completed_quiz_count',
            'completed_assignment_count', 'is_active'
        ]
        read_only_fields = [
            'user', 'enrolled_at', 'is_completed',
            'completed_percentage', 'completed_at',
            'estimate_completion_date', 'completed_lesson_count',
            'completed_quiz_count', 'completed_assignment_count',
            'is_active'
        ]