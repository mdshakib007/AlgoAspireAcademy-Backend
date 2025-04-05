from django.urls import path, include
from apps.account.views import (
    UserLoginView, 
    UserRegistrationView, 
    activate,
    LogoutView,
    EditProfileView,
    ChangePasswordView,
    AccountDeleteView,
    MyDetailsAPIView,

    UserDetailsAPIView,
    UserSummaryAPIView,
)

urlpatterns = [
    # account
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('confirm-email/<uid64>/<token>/', activate, name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('delete/', AccountDeleteView.as_view(), name='delete'),

    # profile summary
    path('me/', MyDetailsAPIView.as_view(), name='details'),
    path('<str:username>/', UserDetailsAPIView.as_view(), name='user-details'),
    path('<str:username>/summary/', UserSummaryAPIView.as_view(), name='user-summary'),
]
