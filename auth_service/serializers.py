# auth_service/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from system_a.models import UserProfile, Department
from system_b.models import UserPreference

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'description')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role')

class UserProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = ('user_id', 'first_name', 'last_name', 'phone_number', 
                 'address', 'department', 'department_id', 'position', 'join_date')

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ('user_id', 'theme', 'language', 'notifications_enabled',
                 'notification_preferences', 'dashboard_layout', 'work_hours')

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    department_id = serializers.IntegerField(required=False)
    position = serializers.CharField(required=False, allow_blank=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)