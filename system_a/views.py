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
            200: openapi.Response(
                "Success response with user and profile data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'user': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_STRING),
                                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                                        'role': openapi.Schema(type=openapi.TYPE_STRING),
                                    }
                                ),
                                'profile': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'department': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                        'position': openapi.Schema(type=openapi.TYPE_STRING),
                                    }
                                )
                            }
                        ),
                        'databases_accessed': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            404: openapi.Response("User or profile not found")
        },
        tags=['System A']
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

    @swagger_auto_schema(
        operation_description="List all user profiles or create a new one",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['first_name', 'last_name', 'position'],
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'position': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            201: UserProfileSerializer,
            400: 'Bad Request'
        },
        tags=['User Profiles']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="List all user profiles",
        responses={200: UserProfileSerializer(many=True)},
        tags=['User Profiles']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

@swagger_auto_schema(tags=['User Profiles'])
class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

    @swagger_auto_schema(
        operation_description="Retrieve a user profile by user ID",
        responses={
            200: UserProfileSerializer,
            404: 'Not Found'
        },
        tags=['User Profiles']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user profile",
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
        tags=['User Profiles']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a user profile",
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
        tags=['User Profiles']
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

@swagger_auto_schema(tags=['Departments'])
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new department",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            201: DepartmentSerializer,
            400: 'Bad Request'
        },
        tags=['Departments']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="List all departments",
        responses={200: DepartmentSerializer(many=True)},
        tags=['Departments']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@swagger_auto_schema(tags=['Departments'])
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a department by ID",
        responses={
            200: DepartmentSerializer,
            404: 'Not Found'
        },
        tags=['Departments']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a department",
        request_body=DepartmentSerializer,
        responses={
            200: DepartmentSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
        tags=['Departments']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a department",
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
        tags=['Departments']
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
