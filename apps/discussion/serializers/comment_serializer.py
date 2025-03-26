from rest_framework import serializers
from apps.account.models import User
from apps.discussion.models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'content']


class CommentListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'username', 'user_image',
            'post', 'content', 'created_at', 'updated_at',
        ]

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    def get_user_image(self, obj):
        if obj.user and obj.user.profile_picture:
            return obj.user.profile_picture.url
        return None