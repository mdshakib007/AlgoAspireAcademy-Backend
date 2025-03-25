from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from apps.course.constants import LectureType, OptionChoices


class BaseModel(models.Model):
    """An abstract model with fields common to most models."""
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Course(BaseModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, null=True, blank=True)
    image = models.URLField()
    description = models.TextField()
    instructor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='courses')

    module_count = models.PositiveIntegerField(default=0)
    lesson_count = models.PositiveIntegerField(default=0)
    assignment_count = models.PositiveIntegerField(default=0)
    quiz_count = models.PositiveIntegerField(default=0)
    enrolled = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.code}-{self.name}")
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'courses'
        indexes = [
            models.Index(fields=['code']), # quick lookup by course code.
            models.Index(fields=['is_published']), # If filtering on published courses.
            models.Index(fields=['instructor']),  # Optimize queries filtering by instructor
        ]
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name}"


class Module(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=150)
    summary = models.TextField()
    lesson_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'modules'
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['is_published'])
        ]
        ordering = ['created_at']

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class Lesson(BaseModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=150)
    summary = models.TextField(null=True, blank=True)
    lecture_type = models.CharField(max_length=20, choices=LectureType.choices) # video, text, quiz, assignment
    video = models.URLField(null=True, blank=True)
    text_editorial = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'lessons'
        indexes = [
            models.Index(fields=['module']),
            models.Index(fields=['is_published']),
            models.Index(fields=['lecture_type']),
        ]
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title}"


class Quiz(BaseModel):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'quizzes'
        indexes = [
            models.Index(fields=['lesson'])
        ]
        ordering = ['created_at']

    def __str__(self):
        return f"{self.lesson.title}"


class Question(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    title = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=OptionChoices.choices)
    explanation = models.TextField()

    class Meta:
        db_table = 'questions'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.quiz.lesson.title} - {self.title[:50]}"


class Assignment(BaseModel):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='assignment')
    title = models.CharField(max_length=100)
    question = models.TextField()
    total_mark = models.PositiveIntegerField(default=10)

    class Meta:
        db_table = 'assignments'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.lesson.title}"