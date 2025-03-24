from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from apps.enrollment.models import LessonCompletion
from apps.course.constants import LectureType


@receiver(post_save, sender=LessonCompletion)
def lesson_completed(sender, instance, created, **kwargs):
    if created:
        enrollment = instance.enrollment
        course = enrollment.course
        module = instance.lesson.module

        # Update lesson count and percentage
        enrollment.completed_lesson_count += 1
        enrollment.completed_percentage = (enrollment.completed_lesson_count / course.lesson_count) * 100

        # Update quiz and assignment count if applicable
        if instance.lesson.lecture_type == LectureType.QUIZ:
            enrollment.completed_quiz_count += 1
        elif instance.lesson.lecture_type == LectureType.ASSIGNMENT:
            enrollment.completed_assignment_count += 1

        # Check if the course is completed
        if enrollment.completed_lesson_count == course.lesson_count:
            enrollment.is_completed = True
            enrollment.completed_at = now()

        enrollment.save(update_fields=[
            'completed_lesson_count', 'completed_percentage', 
            'completed_quiz_count', 'completed_assignment_count',
            'is_completed', 'completed_at'
        ])