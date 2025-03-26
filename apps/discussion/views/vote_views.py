import logging 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response

from apps.discussion.serializers import VoteSerializer
from apps.discussion.models import Vote, Post

logger = logging.getLogger(__name__)


class VotePostView(CreateAPIView):
    serializer_class = VoteSerializer
    queryset = Post.objects.filter(is_deleted=False)

    @swagger_auto_schema(
        tags=['Vote'],
        request_body=VoteSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('Successfully Toggled Vote'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Post not found'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('An error occurred'),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            _post = self.queryset.get(pk=self.request.data.get('post'))
        except Post.DoesNotExist:
            return Response({'error':'Post not found'})
        
        vote, created = Vote.objects.get_or_create(user=request.user, post=_post)

        if not created:
            vote.delete()
            return Response({'success': 'Vote removed!'})
        return Response({'success': 'Vote added!'})