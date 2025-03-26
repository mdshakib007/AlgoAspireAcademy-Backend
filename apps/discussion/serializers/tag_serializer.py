from rest_framework import serializers
from apps.discussion.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [ 'id', 'name', 'slug']