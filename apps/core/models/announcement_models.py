from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    cover = models.URLField(default='https://i.ibb.co.com/PZzz6FrB/announcement.png')
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Announcements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'created_at']),
        ]
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.title