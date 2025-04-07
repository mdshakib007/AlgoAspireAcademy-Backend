from rest_framework import serializers

from apps.account.models import User
from apps.course.models import Course
from .module_serializers import ModuleListSerializer
from apps.enrollment.models import Enrollment


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
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)

    class Meta:
        model = Course 
        fields = [
            'id', 'code', 'name', 'slug', 'image',
            'instructor', 'instructor_name', 'enrolled', 'is_published',
        ]


class CourseDetailsSerializer(serializers.ModelSerializer):
    modules = ModuleListSerializer(many=True, read_only=True)
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    i_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'slug', 'image', 'description', 
            'instructor', 'instructor_name', 'module_count', 'lesson_count', 
            'assignment_count', 'quiz_count', 'modules', 'enrolled', 'i_enrolled',
            'is_published', 'created_at', 'updated_at',
        ]
    
    def get_i_enrolled(self, course):
        user = self.context.get('request').user

        if user.is_authenticated:
            enrollment = Enrollment.objects.filter(user=user, course=course).exists()
            return enrollment
        else:
            return False
