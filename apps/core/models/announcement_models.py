from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    cover = models.URLField(default='https://i.ibb.co.com/PZzz6FrB/announcement.png')
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title