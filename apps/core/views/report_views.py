from rest_framework import status,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView
from django.db.models import F
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from apps.core.serializers import ReportCreateSerializer, ReportListSerializer
from apps.core.models import Report
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger(__name__)


class ReportCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Create a report on any content object",
        request_body=ReportCreateSerializer,
        tags=['Report'],
        responses={
            status.HTTP_201_CREATED: openapi.Response(description="Report created successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid input or content type"),
        }
    )
    def post(self, request):
        serializer = ReportCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            report = serializer.save()
            return Response(ReportListSerializer(report).data, status=status.HTTP_201_CREATED)
        logger.warning("Invalid report data: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class ReportListAPIView(ListAPIView):
    serializer_class = ReportListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Report.objects.all()

        reported_by_id = self.request.query_params.get('reported_by__id')
        content_type_model = self.request.query_params.get('content_type__model')
        is_reviewed = self.request.query_params.get('is_reviewed')

        if reported_by_id:
            queryset = queryset.filter(reported_by__id=reported_by_id)

        if content_type_model:
            queryset = queryset.filter(content_type__model=content_type_model)

        if is_reviewed is not None:
            if is_reviewed.lower() in ['true', '1']:
                queryset = queryset.filter(is_reviewed=True)
            elif is_reviewed.lower() in ['false', '0']:
                queryset = queryset.filter(is_reviewed=False)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'reported_by__id',
                openapi.IN_QUERY,
                description="Filter by reporter user ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'content_type__model',
                openapi.IN_QUERY,
                description="Filter by content type model name (e.g., 'post', 'comment', 'lesson')",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'is_reviewed',
                openapi.IN_QUERY,
                description="Filter by review status (true or false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description='Enable or disable pagination',
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True
            )
        ],
        tags=['Report'],
        operation_summary="Get a filtered list of reports",
        responses={
            status.HTTP_200_OK: openapi.Response(description="List of reports"),
        }
    )   
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
            
        return super().get(request, *args, **kwargs)
