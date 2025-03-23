from rest_framework import serializers

from apps.course.models import Course
from .module_serializers import ModuleListSerializer


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'code', 'name', 
            'image', 'description', 'module_count',
            'lesson_count', 'assignment_count', 
            'quiz_count', 'is_published',
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        instructor = request.user if request else None
        course = Course.objects.create(**validated_data, instructor=instructor)
        course.save()
        return course


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course 
        fields = [
            'id', 'code', 'name', 'slug', 'image',
            'instructor', 'is_published',
        ]


class CourseDetailsSerializer(serializers.ModelSerializer):
    modules = ModuleListSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'slug', 'image', 'description', 
            'instructor', 'module_count', 'lesson_count', 
            'assignment_count', 'quiz_count',
            'is_published', 'created_at', 'updated_at',
        ]