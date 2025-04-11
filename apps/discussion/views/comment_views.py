import logging 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny

from apps.discussion.serializers import CommentCreateSerializer, CommentListSerializer
from apps.discussion.models import Comment, Post

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Comment.objects.filter(is_deleted=False)
        user_id = self.request.query_params.get('user_id')
        post_id = self.request.query_params.get('post_id')

        if user_id:
            queryset = queryset.filter(user=user_id)
        if post_id:
            queryset = queryset.filter(post=post_id)

        return queryset
    
    @swagger_auto_schema(
        tags=['Comment'],
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="Filter by user id",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'post_id',
                openapi.IN_QUERY,
                description="Filter by post id",
                type=openapi.TYPE_INTEGER,
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
            status.HTTP_200_OK: openapi.Response(description='List of comments'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred')
        }
    )
    def get(self, request, *args, **kwargs):
        paginated = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
        
        return super().get(request, *args, **kwargs)


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentCreateSerializer

    @swagger_auto_schema(
        tags=['Comment'],
        request_body=CommentCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Comment created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred')
        }
    )
    def post(self, request, *args, **kwargs):
        # Extract data from the request body
        content = request.data.get('content')
        post_id = request.data.get('post')
        user = request.user
        
        try:
            _post = Post.objects.get(pk=post_id, is_deleted=False)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            new_comment = Comment.objects.create(
                user=user,
                post=_post,
                content=content
            )
            serializer = self.serializer_class(new_comment)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentUpdateAPIView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.filter(is_deleted=False)

    def get_object(self):
        return self.queryset.get(user=self.request.user, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Comment'],
        request_body= CommentCreateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Comment updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Comment not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to update Comment')
        }
    )
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)


class CommentDeleteAPIView(DestroyAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.filter(is_deleted=False)

    def get_object(self):
        return self.queryset.get(user=self.request.user, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        tags=['Comment'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Comment deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Comment not found'),
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save(update_fields=['is_deleted'])
            return Response({'success': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
