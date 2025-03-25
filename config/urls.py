from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.account.views import CookieTokenRefreshView

admin.site.site_header = 'AlgoAspire'


swagger_url_patterns = None
if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="AlgoAspire API",
            default_version='v1',
            description="This is the api documentation of AlgoAspire-Web",
            terms_of_service="https://www.algoaspire.com/terms/",
            contact=openapi.Contact(email="contact@algoaspire.com"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny, ],
        authentication_classes=[SessionAuthentication, JWTAuthentication],
    )
    swagger_url_patterns = [
        path('', lambda request: redirect('/swagger/', permanent=True)),
        path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='refresh-token'),

    path('api/account/', include('apps.account.urls')),
    path('api/course/', include('apps.course.urls')),
    path('api/discussion/', include('apps.discussion.urls')),
    path('api/gamification/', include('apps.gamification.urls')),
    path('api/enrollment/', include('apps.enrollment.urls')),
]

if settings.DEBUG and swagger_url_patterns:
    urlpatterns += swagger_url_patterns
    