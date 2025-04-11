from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from apps.core.models import Report


class ReportCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()
    object_id = serializers.IntegerField()

    class Meta:
        model = Report
        fields = ['content_type', 'object_id', 'issue']

    def create(self, validated_data):
        model_str = validated_data.pop('content_type')
        try:
            content_type = ContentType.objects.get(model=model_str.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({"content_type": "Invalid content type."})

        report = Report.objects.create(
            reported_by=self.context['request'].user,
            content_type=content_type,
            object_id=validated_data['object_id'],
            issue=validated_data.get('issue', '')
        )
        return report


class ReportListSerializer(serializers.ModelSerializer):
    content_type = serializers.StringRelatedField()
    reported_by = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = ['id', 'reported_by', 'content_type', 'object_id', 'issue', 'is_reviewed', 'created_at']
