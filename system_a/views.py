from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Department
from auth_service.services import UserService

# Create your views here.

class SystemATestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.user.id
        
        # Get user profile from MySQL
        profile = UserService.get_user_profile(user_id)
        if not profile:
            return Response({
                'status': 'error',
                'message': 'Profile not found in System A (MySQL)',
                'database': 'MySQL'
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
            'message': 'Authentication and database access working in System A',
            'data': {
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'role': user.role
                },
                'profile': {
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'department': profile.department.name if profile.department else None,
                    'position': profile.position
                }
            },
            'databases_accessed': ['PostgreSQL', 'MySQL']
        })
