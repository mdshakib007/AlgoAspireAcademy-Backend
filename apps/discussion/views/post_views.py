import logging 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

from apps.discussion.serializers import PostCreateSerializer, PostDetailsSerializer, PostListSerializer
from apps.discussion.models import Post

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Post.objects.filter(is_deleted=False)
        user_id = self.request.query_params.get('user_id')
        lesson_id = self.request.query_params.get('lesson_id')
        post_type = self.request.query_params.get('post_type')
        access_type = self.request.query_params.get('access')

        if user_id:
            queryset = queryset.filter(user=user_id)
        if lesson_id:
            queryset = queryset.filter(lesson=lesson_id)
        if post_type:
            queryset = queryset.filter(post_type=post_type.lower())
        if access_type:
            queryset = queryset.filter(access=access_type.lower())

        return queryset
    
    @swagger_auto_schema(
        tags=['Post'],
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="Filter by user id",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'lesson_id',
                openapi.IN_QUERY,
                description="Filter by lesson id",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'post_type',
                openapi.IN_QUERY,
                description="Filter by post type(Note, Question, Feedback, Editorial, Announcement, Tutorial)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'access_type',
                openapi.IN_QUERY,
                description="Filter by access type(Public, Private)",
                type=openapi.TYPE_STRING,
                required=False
            ),
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
            status.HTTP_200_OK: openapi.Response(description='List of courses'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred')
        }
    )
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
        
        return super().get(request, *args, **kwargs)


class PostDetailsAPIView(RetrieveAPIView):
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostDetailsSerializer

    def get_object(self):
        post_id = self.kwargs.get('pk')

        try:
            post = self.queryset.get(pk=post_id)
        except Post.DoesNotExist:
            raise NotFound('Post not found')

        return post

    @swagger_auto_schema(
        tags=['Post'],
        responses={
            status.HTTP_200_OK: openapi.Response(description='Post details'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Post not found')
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            post = self.get_object()
            serializer = self.get_serializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'error':'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    

class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer

    @swagger_auto_schema(
        tags=['Post'],
        request_body= PostCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Post created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred')
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostUpdateAPIView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = PostCreateSerializer
    queryset = Post.objects.filter(is_deleted=False)

    def get_object(self):
        return self.queryset.get(user=self.request.user, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Post'],
        request_body= PostCreateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Post updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Post not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to update Post')
        }
    )
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class PostDeleteAPIView(DestroyAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.filter(is_deleted=False)

    def get_object(self):
        return self.queryset.get(user=self.request.user, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Post'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Post deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Post not found'),
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save(update_fields=['is_deleted'])
            return Response({'success': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
