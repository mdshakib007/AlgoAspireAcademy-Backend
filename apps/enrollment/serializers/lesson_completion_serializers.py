from rest_framework import serializers

from apps.enrollment.models import LessonCompletion
from apps.course.serializers import LessonListSerializer
from apps.course.constants import LectureType


class LessonCompletionSerializer(serializers.ModelSerializer):
    lecture_type = serializers.SerializerMethodField()

    class Meta:
        model = LessonCompletion
        fields = [
            'enrollment', 'lesson', 'lecture_type', 'quiz_answers',
            'quiz_marks', 'assignment_submission',
            'assignment_marks', 'completed_at',
        ]
        read_only_fields = ['completed_at']

    def get_lecture_type(self, obj):
        return LessonListSerializer(obj.lesson).data.get('lecture_type')


class LessonCompletionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonCompletion
        fields = [
            'enrollment', 'lesson', 'quiz_answers',
            'assignment_submission', 
        ]