from django.db import models 

class LectureType(models.TextChoices):
    VIDEO = 'video', 'Video'
    TEXT = 'text', 'Text'
    QUIZ = 'quiz', 'Quiz'
    ASSIGNMENT = 'assignment', 'Assignment'

class OptionChoices(models.TextChoices):
    A = 'a', 'A'
    B = 'b', 'B'
    C = 'c', 'C'
    D = 'd', 'D'