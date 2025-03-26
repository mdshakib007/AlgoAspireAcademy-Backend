from rest_framework import serializers
from apps.discussion.models import Post
from apps.account.models import User


class PostListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'username', 'user_image',
            'lesson', 'title', 'post_type', 'views',
            'vote_count', 'comment_count', 'access', 
            'tags', 'created_at',
        ]

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    def get_user_image(self, obj):
        if obj.user and obj.user.profile_picture:
            return obj.user.profile_picture.url
        return None


class PostDetailsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'username', 'user_image',
            'lesson', 'title', 'body', 'post_type', 
            'views', 'vote_count', 'comment_count', 
            'access', 'tags', 'created_at', 'updated_at',
        ]

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    def get_user_image(self, obj):
        if obj.user and obj.user.profile_picture:
            return obj.user.profile_picture.url
        return None


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'lesson', 'title', 'body',
            'post_type', 'access', 'tags',
        ]