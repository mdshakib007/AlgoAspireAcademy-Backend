from django.db import models 

class LectureType(models.TextChoices):
    VIDEO = 'Video', 'Video'
    TEXT = 'Text', 'Text'
    QUIZ = 'Quiz', 'Quiz'
    ASSIGNMENT = 'Assignment', 'Assignment'