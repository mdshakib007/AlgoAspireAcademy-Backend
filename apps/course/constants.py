from django.db import models 

class LectureType(models.TextChoices):
    VIDEO = 'video', 'video'
    TEXT = 'text', 'text'
    QUIZ = 'quiz', 'quiz'
    ASSIGNMENT = 'assignment', 'assignment'