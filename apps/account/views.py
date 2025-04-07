import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.account.models import User
from apps.account.serializers import (
    UserLoginSerializer, 
    UserRegistrationSerializer, 
    ChangePasswordSerializer, 
    UserProfileUpdateSerializer,
    UserDetailsSerializer,
    UserSummarySerializer,
) 

logger = logging.getLogger(__name__)



class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Account'],
        request_body=UserRegistrationSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='User created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred')
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/api/account/confirm-email/{uid}/{token}/"

            subject = "Confirm Your Email"
            email_body = render_to_string('account/confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(subject, email_body, settings.EMAIL_HOST_USER, [user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response({'success': 'Please check your email for confirmation!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'account/email_confirmed.html')
    
    return render(request, 'account/email_not_confirmed.html')


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Account'],
        request_body=UserLoginSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Login successful'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Account not found')
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                "access": access_token,  # Frontend should store this in memory
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "profile_picture": user.profile_picture
                }
            }, status=status.HTTP_200_OK)

            # Store refresh token in HttpOnly cookie
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,  # Prevents JavaScript access (XSS protection)
                secure=True,  # Send only over HTTPS in production
                samesite="Lax",  # Helps prevent CSRF issues
            )

            return response
        
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CookieTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['Token'],
        responses={
            status.HTTP_401_UNAUTHORIZED: "You are not authorized!",
            status.HTTP_200_OK: "Token refreshed",
        }
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Inject the refresh token from the cookie into the request data.
        request.data["refresh"] = refresh_token
        
        # Call the parent view to get the new tokens.
        response = super().post(request, *args, **kwargs)
        
        # If a new refresh token is issued, update the HttpOnly cookie.
        if "refresh" in response.data:
            new_refresh = response.data.pop("refresh")  # Removed from response data.
            response.set_cookie(
                key="refresh_token",
                value=new_refresh,
                httponly=True,     # Ensures the cookie is not accessible via JavaScript.
                secure=True,       # Use HTTPS in production.
                samesite="Lax",    # Helps protect against CSRF.
            )
        
        return response


class LogoutView(APIView):
    @swagger_auto_schema(
        tags=['Account'],
        responses={
            status.HTTP_200_OK: "Logout Successful",
            status.HTTP_401_UNAUTHORIZED: "Authentication crediential not provided",
        }
    )
    def post(self, request):
        response = Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")  # clear the refresh token cookie
        return response


class AccountDeleteView(APIView):
    @swagger_auto_schema(
        tags=['Account'],
        responses={
            status.HTTP_200_OK: "Account deleted successfully",
            status.HTTP_400_BAD_REQUEST: "An error occurred"
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.is_deleted = True
        user.save(update_fields=["is_active", "is_deleted"])
        return Response({"detail": "Account deleted successfully."}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={
            status.HTTP_200_OK: "Password changed successfully",
            status.HTTP_400_BAD_REQUEST: "Validation errors"
        },
        tags=['Account']
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfileView(APIView):
    http_method_names = ['put']
    @swagger_auto_schema(
        tags=['Account'],
        request_body=UserProfileUpdateSerializer,
        responses={
            status.HTTP_200_OK: "Profile updated successfully",
            status.HTTP_400_BAD_REQUEST: "Validation errors"
        },
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Profile updated successfully", "user": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyDetailsAPIView(APIView):
    serializer_class = UserDetailsSerializer

    @swagger_auto_schema(
        tags=['Profile'],
        responses={
            status.HTTP_200_OK: UserDetailsSerializer,
            status.HTTP_401_UNAUTHORIZED: "Authentication credentials were not provided."
        }
    )
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class UserDetailsAPIView(APIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Profile'],
        responses={
            status.HTTP_200_OK: UserDetailsSerializer(),
            status.HTTP_404_NOT_FOUND: "User not found.",
            status.HTTP_400_BAD_REQUEST: "This profile is private."
        }
    )
    def get(self, request, username, *args, **kwargs):
        """
        Get user details by username.
        """
        user = get_object_or_404(User, username=username, is_active=True, is_deleted=False)
        if user.is_private and request.user != user:
            return Response({'details': 'This profile is private'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSummaryAPIView(APIView):
    serializer_class = UserSummarySerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Profile'],
        responses={
            status.HTTP_200_OK: UserSummarySerializer(),
            status.HTTP_404_NOT_FOUND: "User not found.",
            status.HTTP_400_BAD_REQUEST: "This profile is private."
        }
    )
    def get(self, request, username, *args, **kwargs):
        """
        Get user summary by username.
        """
        user = get_object_or_404(User, username=username, is_active=True, is_deleted=False)
        if user.is_private and request.user != user:
            return Response({'details': 'This profile is private'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)