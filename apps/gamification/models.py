from django.db import models

from apps.account.models import User
from apps.gamification.constants import Titles, Activity, Badge, Achievement


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserAchievement(BaseModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='achievement')

    neons = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=100, choices=Titles.choices, default="Merry Beginner")
    badges = models.ManyToManyField('Badge', blank=True)
    achievements = models.ManyToManyField('Achievement', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class UserActivityLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    activity_type = models.CharField(max_length=100, choices=Activity.choices)
    neon_earned = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - (+{self.neon_earned} Neon)"


class Badge(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='badges')
    badge_type = models.CharField(max_length=100, choices=Badge.choices)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge_type}"


class Achievement(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='achievements')
    achievement_type = models.CharField(max_length=100, choices=Achievement.choices)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement_type}"
    