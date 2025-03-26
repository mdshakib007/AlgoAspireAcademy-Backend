import logging 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from apps.discussion.serializers import TagSerializer
from apps.discussion.models import Tag

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class TagListAPIView(ListAPIView):
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=['Tag'],
        manual_parameters=[
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description="Enable or disable pagination (true or false)",
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response('Tag list'),
        }
    )
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
            
        return super().get(request, *args, **kwargs)