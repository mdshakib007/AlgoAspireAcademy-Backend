from django.urls import path
from apps.core.views import (
    LatestAnnouncementAPIView, 
    RecentAnnouncementsAPIView, 
    AnnouncementDetailAPIView,
    ReportCreateAPIView,
    ReportListAPIView,
)


urlpatterns = [
    # announcement 
    path('announcement/latest/', LatestAnnouncementAPIView.as_view(), name='latest-announcement'),
    path('announcement/recent/', RecentAnnouncementsAPIView.as_view(), name='recent-announcement'),
    path('announcement/<int:pk>/', AnnouncementDetailAPIView.as_view(), name='details-announcement'),

    # report
    path('report/create/', ReportCreateAPIView.as_view(), name='report-create'),
    path('report/list/', ReportListAPIView.as_view(), name='report-list'),
]
