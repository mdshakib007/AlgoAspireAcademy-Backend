from django.urls import path, include
from apps.account.views import (
    UserLoginView, 
    UserRegistrationView, 
    activate,
    LogoutView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('confirm-email/<uid64>/<token>/', activate, name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
