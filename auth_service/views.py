# auth_service/views.py
import jwt
import datetime
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    UserSerializer, UserProfileSerializer, UserPreferenceSerializer, 
    UserRegistrationSerializer, LoginSerializer
)
from .services import UserService

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            201: openapi.Response('User registered successfully'),
            400: openapi.Response('Bad request')
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                user = UserService.create_user(
                    email=data['email'],
                    password=data['password'],
                    first_name=data.get('first_name', ''),
                    last_name=data.get('last_name', ''),
                    phone_number=data.get('phone_number', ''),
                    address=data.get('address', '')
                )
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Login with email and password to get JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            }
        ),
        responses={
            200: openapi.Response(
                'Login successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: openapi.Response('Invalid credentials')
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get user profile data including preferences",
        responses={
            200: UserSerializer,
            404: openapi.Response('User not found')
        },
        tags=['User Profile']
    )
    def get(self, request):
        user_id = request.user.id
        
        # Fetch user data from PostgreSQL
        user = UserService.get_user(user_id)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user_data = UserSerializer(user).data
        
        # Lazy load additional user data from MySQL
        profile = UserService.get_user_profile(user_id)
        if profile:
            user_data['profile'] = UserProfileSerializer(profile).data
        
        # Lazy load user preferences from MongoDB
        preferences = UserService.get_user_preferences(user_id)
        if preferences:
            user_data['preferences'] = UserPreferenceSerializer(preferences).data
        
        return Response(user_data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Update user profile and preferences",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'profile': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                        'address': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                'preferences': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'theme': openapi.Schema(type=openapi.TYPE_STRING),
                        'language': openapi.Schema(type=openapi.TYPE_STRING),
                        'notifications_enabled': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            }
        ),
        responses={
            200: openapi.Response('User data updated successfully'),
            400: openapi.Response('Bad request')
        },
        tags=['User Profile']
    )
    def patch(self, request):
        user_id = request.user.id
        
        # Update user profile data
        profile_data = request.data.get('profile', {})
        if profile_data:
            profile = UserService.update_user_profile(user_id, **profile_data)
        
        # Update user preferences
        preferences_data = request.data.get('preferences', {})
        if preferences_data:
            preferences = UserService.update_user_preferences(user_id, **preferences_data)
        
        return Response({'message': 'User data updated successfully'}, status=status.HTTP_200_OK)