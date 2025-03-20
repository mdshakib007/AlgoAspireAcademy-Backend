from rest_framework import serializers

from apps.course.models import Assignment


class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'lesson', 'question', 'total_mark',
        ]


class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'id', 'lesson', 'title', 'total_mark'
        ]


class AssignmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'id', 'lesson', 'title', 'question',
            'answer', 'total_mark', 'obtained_mark',
            'is_completed'
        ]