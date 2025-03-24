from rest_framework import serializers

from apps.enrollment.models import LessonCompletion


class LessonCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonCompletion
        fields = ['enrollment', 'lesson', 'completed_at']
        read_only_fields = ['completed_at']