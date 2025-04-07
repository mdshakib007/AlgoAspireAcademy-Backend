from rest_framework import serializers
from apps.core.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'cover', 'message', 'created_at']
