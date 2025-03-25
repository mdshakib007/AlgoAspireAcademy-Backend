from django.db import models

class DiscussionTypes(models.TextChoices):
    NOTE = 'Note', 'Note'
    QUESTION = 'Question', 'Question'
    FEEDBACK = 'Feedback', 'Feedback'
    EDITORIAL = 'Editorial', 'Editorial'
    ANNOUNCEMENT = 'Announcement', 'Announcement'
    TUTORIAL = 'Tutorial', 'Tutorial'


class AccessTypes(models.TextChoices):
    PUBLIC = 'Public', 'Public'
    PRIVATE = 'Private', 'Private'