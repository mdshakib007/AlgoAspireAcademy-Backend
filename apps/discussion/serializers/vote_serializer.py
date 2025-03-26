from rest_framework import serializers
from apps.discussion.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['user', 'post']
        read_only_fields = ['user']