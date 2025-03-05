from rest_framework import serializers
from apps.course.models import (
    Course, 
    Module, 
    Lesson, 
    Quiz, 
    Question, 
    Assignment
)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 
            'title', 
            'option_1', 
            'option_2', 
            'option_3', 
            'option_4', 
            'correct_option', 
            'explanation'
        ]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'lesson', 'questions']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'id', 
            'lesson', 
            'question', 
            'answer', 
            'total_mark', 
            'obtained_mark'
        ]

class LessonSerializer(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()
    assignment = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 
            'title', 
            'summary', 
            'lecture_type', 
            'video', 
            'text_editorial', 
            'quiz', 
            'assignment'
        ]
    
    def get_quiz(self, obj):
        try:
            return QuizSerializer(obj.quiz).data
        except Quiz.DoesNotExist:
            return None

    def get_assignment(self, obj):
        try:
            return AssignmentSerializer(obj.assignment).data
        except Assignment.DoesNotExist:
            return None

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            'id', 
            'title', 
            'summary', 
            'completed_lessons_count', 
            'lessons'
        ]

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 
            'code', 
            'name', 
            'slug', 
            'image', 
            'description', 
            'instructor', 
            'is_enrolled',
            'completed_modules_count', 
            'completed_assignments_count', 
            'completed_quizzes_count', 
            'modules'
        ]

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course 
        fields = [
            'id',
            'code',
            'name',
            'slug',
            'image',
            'instructor',
            'is_enrolled',
        ]

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'code',
            'name',
            'image',
            'description',
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        instructor = request.user if request else None
        course = Course.objects.create(**validated_data, instructor=instructor)
        course.save()
        return course
