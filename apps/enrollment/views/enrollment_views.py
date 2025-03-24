from django.contrib.auth import get_user_model
import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from apps.enrollment.models import Enrollment
from apps.enrollment.serializers import EnrollmentSerializer
from apps.course.models import Course

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class EnrollmentListAPIView(ListAPIView):
    serializer_class = EnrollmentSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Enrollment.objects.all()
        user_id = self.request.query_params.get('user_id')
        course_id = self.request.query_params.get('course_id')
        is_active = self.request.query_params.get('is_active')

        if user_id:
            queryset = queryset.filter(user=user_id)
        if course_id:
            queryset = queryset.filter(course=course_id)
        if is_active:
            active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=active)
        return queryset

    @swagger_auto_schema(
        tags=['Enrollment'],
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description='Filter by user id',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'course_id',
                openapi.IN_QUERY,
                description='Filter by course id',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description='Filter by active',
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True,
            ),
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description='Enable or disable pagination',
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None

        return super().get(request, *args, **kwargs)


class EnrollmentDetailsAPIView(RetrieveAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    @swagger_auto_schema(
        tags=['Enrollment'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='enrollment details'
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description='You are not authorized to view'
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Not found'
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='An error occurred'
            )
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            enrollment = self.get_object()
            serializer = self.get_serializer(enrollment)
            return Response(serializer.data, status.HTTP_200_OK)
        except Enrollment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get_object(self):
        id = self.kwargs.get('pk')
        
        try:
            return self.queryset.get(pk=id)
        except Enrollment.DoesNotExist:
            raise NotFound("Enrollment not found")


class EnrollmentCreateAPIView(CreateAPIView):
    serializer_class = EnrollmentSerializer

    @swagger_auto_schema(
        tags=['Enrollment'],
        request_body=EnrollmentSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Enrollment created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='You are not authorized to create enrollment')
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')

        if not course_id:
            return Response({"error": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already enrolled in the course
        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({"error": "You are already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the enrollment
        enrollment = Enrollment.objects.create(user=user, course=course)

        return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)


class EnrollmentDeleteAPIView(DestroyAPIView):
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Enrollment'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Enrollment deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Enrollment not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to delete')
        }
    )
    def delete(self, request, *args, **kwargs):
        if request.user.is_instructor:
            return self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({'success': 'Enrollment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Enrollment not found'}, status=status.HTTP_404_NOT_FOUND)