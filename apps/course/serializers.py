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
    quiz = QuizSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)

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
            'completed_modules_count', 
            'completed_assignments_count', 
            'completed_quizzes_count', 
            'modules'
        ]