from rest_framework import serializers

from apps.course.models import Course
from .module_serializers import ModuleListSerializer


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'code', 'name', 'image', 'description',
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
            'instructor', 'is_enrolled',
        ]


class CourseDetailsSerializer(serializers.ModelSerializer):
    modules = ModuleListSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'slug', 'image', 'description', 
            'instructor', 'is_enrolled', 'completed_modules_count', 
            'completed_assignments_count', 'completed_quizzes_count', 
            'modules'
        ]