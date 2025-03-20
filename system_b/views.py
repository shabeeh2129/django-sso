from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserPreference
from auth_service.services import UserService

# Create your views here.

class SystemBTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.user.id
        
        # Get user preferences from MongoDB
        preferences = UserService.get_user_preferences(user_id)
        if not preferences:
            return Response({
                'status': 'error',
                'message': 'Preferences not found in System B (MongoDB)',
                'database': 'MongoDB'
            }, status=404)
        
        # Get user data from PostgreSQL
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
