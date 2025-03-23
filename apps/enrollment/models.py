from django.db import models
from django.contrib.auth import get_user_model

from apps.course.models import Course, Module, Lesson

student = get_user_model()

class Enrollment(models.Model):
    user = models.ForeignKey(student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Enrollments'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['course']),
            models.Index(fields=['user', 'course']),
        ]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"


class LessonCompletion(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_completions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_completions')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('enrollment', 'lesson')
        indexes = [
            models.Index(fields=['enrollment']),
            models.Index(fields=['lesson']),
            models.Index(fields=['enrollment', 'lesson']),
        ]
        verbose_name = "Lesson Completion"
        verbose_name_plural = "Lesson Completions"
        db_table = 'Lesson Completions'


class ModuleCompletion(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='module_completions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module_completions')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['enrollment']),
            models.Index(fields=['module']),
            models.Index(fields=['enrollment', 'module']),
        ]
        verbose_name = "Module Completion"
        verbose_name_plural = "Module Completions"
        db_table = 'Module Completions'