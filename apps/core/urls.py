from django.urls import path
from apps.core.views import LatestAnnouncementAPIView, RecentAnnouncementsAPIView, AnnouncementDetailAPIView


urlpatterns = [
    path('announcement/latest/', LatestAnnouncementAPIView.as_view(), name='latest-announcement'),
    path('announcement/recent/', RecentAnnouncementsAPIView.as_view(), name='recent-announcement'),
    path('announcement/<int:pk>/', AnnouncementDetailAPIView.as_view(), name='details-announcement'),
]
