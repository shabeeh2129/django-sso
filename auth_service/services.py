# auth_service/services.py
from django.core.cache import cache
from django.db import transaction
from django.contrib.auth import get_user_model
from system_a.models import UserProfile, Department
from system_b.models import UserPreference

User = get_user_model()

class UserService:
    @staticmethod
    def get_user(user_id):
        cache_key = f'user_{user_id}'
        user = cache.get(cache_key)
        if not user:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass
            if user:
                cache.set(cache_key, user, 3600)
        return user
    
    @staticmethod
    def get_user_profile(user_id):
        cache_key = f'profile_{user_id}'
        profile = cache.get(cache_key)
        if not profile:
            try:
                profile = UserProfile.objects.get(user_id=user_id)
            except UserProfile.DoesNotExist:
                pass
            if profile:
                cache.set(cache_key, profile, 3600)
        return profile
    
    @staticmethod
    def get_user_preferences(user_id):
        cache_key = f'preferences_{user_id}'
        preferences = cache.get(cache_key)
        if not preferences:
            try:
                preferences = UserPreference.objects.get(user_id=user_id)
            except UserPreference.DoesNotExist:
                pass
            if preferences:
                cache.set(cache_key, preferences, 3600)
        return preferences
    
    @staticmethod
    @transaction.atomic
    def create_user(email, password, **extra_fields):
        """Create a new user with profile and preferences."""
        # Create auth user in PostgreSQL
        user = User.objects.create_user(email=email, password=password)
        
        # Get department if provided
        department_id = extra_fields.pop('department_id', None)
        department = None
        if department_id:
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                pass

        # Create user profile in MySQL
        UserProfile.objects.create(
            user_id=user.id,
            department=department,
            **extra_fields
        )

        # Create user preferences in MongoDB with defaults
        UserPreference.objects.create(user_id=user.id)

        return user
    
    @staticmethod
    def update_user_auth(user_id, **kwargs):
        user = User.objects.get(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()

        cache.delete(f'user_{user_id}')
        return user
    
    @staticmethod
    def update_user_profile(user_id, **profile_data):
        """Update user profile in MySQL."""
        profile = UserProfile.objects.get(user_id=user_id)
        
        # Handle department update
        department_id = profile_data.pop('department_id', None)
        if department_id:
            try:
                department = Department.objects.get(id=department_id)
                profile.department = department
            except Department.DoesNotExist:
                pass

        # Update other fields
        for key, value in profile_data.items():
            setattr(profile, key, value)
        
        profile.save()
        cache.delete(f'profile_{user_id}')
        return profile
    
    @staticmethod
    def update_user_preferences(user_id, **preferences_data):
        """Update user preferences in MongoDB."""
        preferences = UserPreference.objects.get(user_id=user_id)
        for key, value in preferences_data.items():
            setattr(preferences, key, value)
        preferences.save()
        cache.delete(f'preferences_{user_id}')
        return preferences