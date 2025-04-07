from django.urls import path
from apps.core.views import LatestAnnouncementAPIView


urlpatterns = [
    path('announcement/latest/', LatestAnnouncementAPIView.as_view(), name='latest-announcement'),
]
