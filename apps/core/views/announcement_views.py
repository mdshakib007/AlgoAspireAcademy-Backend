from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging

from apps.core.models import Announcement
from apps.core.serializers import AnnouncementSerializer

logger = logging.getLogger(__name__)


class LatestAnnouncementAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Announcement'],
        responses={
            status.HTTP_200_OK: openapi.Response('Latest announcement'),
            status.HTTP_404_NOT_FOUND: openapi.Response('No running announcement')
        }
    )
    def get(self, request):
        announcement = Announcement.objects.filter(is_active=True).order_by('-created_at').first()
        if announcement:
            return Response(AnnouncementSerializer(announcement).data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)