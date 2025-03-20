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
from .serializers import (
    UserSerializer, UserProfileSerializer, UserPreferenceSerializer, 
    UserRegistrationSerializer, LoginSerializer
)
from .services import UserService

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
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