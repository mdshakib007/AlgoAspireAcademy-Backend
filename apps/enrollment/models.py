from django.db import models
from django.contrib.auth import get_user_model

from apps.course.models import Course, Module, Lesson

student = get_user_model()


class Enrollment(models.Model):
    user = models.ForeignKey(student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_percentage = models.DecimalField(default=0.0, decimal_places=2, max_digits=5) # (completed_lesson / total_lesson) * 100
    completed_at = models.DateTimeField(null=True, blank=True)
    estimate_completion_date = models.DateTimeField(null=True, blank=True)
    completed_lesson_count = models.PositiveIntegerField(default=0)
    completed_quiz_count = models.PositiveIntegerField(default=0)
    completed_assignment_count = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Enrollments'
        unique_together = ('user', 'course', 'is_active')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['course']),
            models.Index(fields=['is_active']),
            models.Index(fields=['user', 'course']),
        ]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"


class LessonCompletion(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_completions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_completions')
    quiz_answers = models.JSONField(null=True, blank=True)
    quiz_marks = models.PositiveIntegerField(null=True, blank=True)
    assignment_submission = models.URLField(null=True, blank=True)
    assignment_marks = models.PositiveIntegerField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('enrollment', 'lesson')
        ordering = ['-completed_at']
        indexes = [
            models.Index(fields=['enrollment']),
            models.Index(fields=['lesson']),
            models.Index(fields=['enrollment', 'lesson']),
        ]
        verbose_name = "Lesson Completion"
        verbose_name_plural = "Lesson Completions"
        db_table = 'Lesson Completions'