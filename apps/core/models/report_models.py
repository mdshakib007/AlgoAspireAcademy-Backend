from django.db import models
from apps.course.models import Lesson
from apps.discussion.models import Post, Comment
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Report(models.Model):
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    issue = models.CharField(max_length=200, null=True, blank=True)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.content_type} (ID: {self.object_id})"

    class Meta:
        db_table = 'core_report'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['reported_by']),
            models.Index(fields=['is_reviewed']),
            models.Index(fields=['created_at']),
        ]
