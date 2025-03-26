from django.urls import path
from apps.discussion.views import (
    PostCreateAPIView,
    PostDeleteAPIView,
    PostDetailsAPIView,
    PostListAPIView,
    PostUpdateAPIView,

    CommentCreateAPIView,
    CommentDeleteAPIView,
    CommentListAPIView,
    CommentUpdateAPIView,

    TagListAPIView,
    VotePostView,
)

urlpatterns = [
    # post
    path('post/list/', PostListAPIView.as_view(), name='post-list'),
    path('post/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('post/details/<int:pk>/', PostDetailsAPIView.as_view(), name='post-details'),
    path('post/delete/<int:pk>/', PostDeleteAPIView.as_view(), name='post-delete'),
    path('post/edit/<int:pk>/', PostUpdateAPIView.as_view(), name='post-edit'),

    # comment
    path('comment/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comment/list/', CommentListAPIView.as_view(), name='comment-list'),
    path('comment/edit/<int:pk>/', CommentUpdateAPIView.as_view(), name='comment-edit'),
    path('comment/delete/<int:pk>/', CommentDeleteAPIView.as_view(), name='comment-delete'),

    # tags
    path('tag/list/', TagListAPIView.as_view(), name='tag-list'),

    # vote
    path('toggle-vote/', VotePostView.as_view(), name='vote-toggle'),
]
