from rest_framework import serializers

from apps.course.models import Assignment


class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'lesson', 'question', 'total_mark', 'is_published',
        ]


class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'id', 'lesson', 'title', 'total_mark', 'is_published', 
        ]


class AssignmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'id', 'lesson', 'title', 'question',
            'answer', 'total_mark', 'obtained_mark',
            'is_completed', 'is_published', 
            'created_at', 'updated_at',
        ]