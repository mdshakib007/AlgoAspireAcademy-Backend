from django.db import models

class PostTypes(models.TextChoices):
    NOTE = 'note', 'Note'
    QUESTION = 'question', 'Question'
    FEEDBACK = 'feedback', 'Feedback'
    EDITORIAL = 'editorial', 'Editorial'
    ANNOUNCEMENT = 'announcement', 'Announcement'
    TUTORIAL = 'tutorial', 'Tutorial'


class AccessTypes(models.TextChoices):
    PUBLIC = 'public', 'Public'
    PRIVATE = 'private', 'Private'