from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserPreference
from auth_service.services import UserService
from auth_service.serializers import UserPreferenceSerializer
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SystemBTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Test endpoint for System B",
        responses={
            200: openapi.Response(
                "Success response with user and preferences data",
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
                                'preferences': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'theme': openapi.Schema(type=openapi.TYPE_STRING),
                                        'language': openapi.Schema(type=openapi.TYPE_STRING),
                                        'notifications_enabled': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                        'notification_preferences': openapi.Schema(type=openapi.TYPE_OBJECT),
                                        'dashboard_layout': openapi.Schema(type=openapi.TYPE_OBJECT),
                                        'work_hours': openapi.Schema(type=openapi.TYPE_OBJECT),
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
            404: openapi.Response("User or preferences not found")
        },
        tags=['System B']
    )
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

@swagger_auto_schema(tags=['User Preferences'])
class UserPreferenceListCreateView(generics.ListCreateAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create new user preferences",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['theme', 'language'],
            properties={
                'theme': openapi.Schema(type=openapi.TYPE_STRING, description="UI theme (e.g., 'light', 'dark')"),
                'language': openapi.Schema(type=openapi.TYPE_STRING, description="Preferred language code (e.g., 'en', 'es')"),
                'notifications_enabled': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'notification_preferences': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'push': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'sms': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                ),
                'dashboard_layout': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'widgets': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        ),
                        'layout': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                ),
                'work_hours': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'start': openapi.Schema(type=openapi.TYPE_STRING),
                        'end': openapi.Schema(type=openapi.TYPE_STRING),
                        'timezone': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            }
        ),
        responses={
            201: UserPreferenceSerializer,
            400: 'Bad Request'
        },
        tags=['User Preferences']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="List all user preferences",
        responses={200: UserPreferenceSerializer(many=True)},
        tags=['User Preferences']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

@swagger_auto_schema(tags=['User Preferences'])
class UserPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

    @swagger_auto_schema(
        operation_description="Retrieve user preferences by user ID",
        responses={
            200: UserPreferenceSerializer,
            404: 'Not Found'
        },
        tags=['User Preferences']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update user preferences",
        request_body=UserPreferenceSerializer,
        responses={
            200: UserPreferenceSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
        tags=['User Preferences']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update user preferences",
        request_body=UserPreferenceSerializer,
        responses={
            200: UserPreferenceSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
        tags=['User Preferences']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete user preferences",
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
        tags=['User Preferences']
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
