from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver
from django.utils.timezone import now

from apps.enrollment.models import Enrollment


@receiver(post_save, sender=Enrollment)
def course_enrolled(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        course.enrolled = F('enrolled') + 1
        course.save(update_fields=['enrolled'])