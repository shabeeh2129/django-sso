from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserPreference
from auth_service.services import UserService
from auth_service.serializers import UserPreferenceSerializer
from rest_framework import generics, status


class SystemBTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.user.id
        
        preferences = UserService.get_user_preferences(user_id)
        if not preferences:
            return Response({
                'status': 'error',
                'message': 'Preferences not found in System B (MongoDB)',
                'database': 'MongoDB'
            }, status=404)
        
        user = UserService.get_user(user_id)
        if not user:
            return Response({
                'status': 'error',
                'message': 'User not found in Auth Service (PostgreSQL)',
                'database': 'PostgreSQL'
            }, status=404)
        
        return Response({
            'status': 'success',
            'message': 'Authentication and database access working in System B',
            'data': {
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'role': user.role
                },
                'preferences': {
                    'theme': preferences.theme,
                    'language': preferences.language,
                    'notifications_enabled': preferences.notifications_enabled,
                    'notification_preferences': preferences.notification_preferences,
                    'dashboard_layout': preferences.dashboard_layout,
                    'work_hours': preferences.work_hours
                }
            },
            'databases_accessed': ['PostgreSQL', 'MongoDB']
        })

class UserPreferenceListCreateView(generics.ListCreateAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

class UserPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'
