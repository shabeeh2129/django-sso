from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Department
from auth_service.services import UserService
from auth_service.serializers import UserProfileSerializer, DepartmentSerializer
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SystemATestView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Test endpoint for System A",
        responses={
            200: "Success response with user and profile data",
            404: "User or profile not found"
        }
    )
    def get(self, request):
        user_id = request.user.id
        
        profile = UserService.get_user_profile(user_id)
        if not profile:
            return Response({
                'status': 'error',
                'message': 'Profile not found in System A (MySQL)',
                'database': 'MySQL'
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

@swagger_auto_schema(tags=['User Profiles'])
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

@swagger_auto_schema(tags=['User Profiles'])
class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

@swagger_auto_schema(tags=['Departments'])
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

@swagger_auto_schema(tags=['Departments'])
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
