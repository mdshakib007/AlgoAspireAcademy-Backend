from django.db import models
from django.template.defaultfilters import slugify

from apps.account.models import User
from apps.course.models import Lesson
from apps.discussion.constants import DiscussionTypes, AccessTypes


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=250)
    body = models.TextField()
    post_type = models.CharField(max_length=20, choices=DiscussionTypes.choices)
    access = models.CharField(max_length=10, choices=AccessTypes.choices, default=AccessTypes.PUBLIC)
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Posts'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['lesson']),
            models.Index(fields=['post_type']),
            models.Index(fields=['user', 'lesson']),
            models.Index(fields=['user', 'lesson', 'post_type'])
        ]
        ordering = ['-created_at']

    def vote_count(self):
        return self.votes.count()
    
    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return f"{self.title}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')

    class Meta:
        db_table = 'Votes'
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['post']),
        ]

    def __str__(self):
        return f"{self.user.username} upvoted on {self.post.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'
        ordering =['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['post']),
            models.Index(fields=['user', 'post']),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"