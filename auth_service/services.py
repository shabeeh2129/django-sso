# auth_service/services.py
from django.core.cache import cache
from django.db import transaction
from django.contrib.auth import get_user_model
from system_a.models import UserProfile
from system_b.models import UserPreference

User = get_user_model()

class UserService:
    @staticmethod
    def get_user(user_id):
        cache_key = f'user_{user_id}'
        user = cache.get(cache_key)
        if not user:
            user = User.objects.filter(id=user_id).first()
            if user:
                cache.set(cache_key, user, 3600)
        return user
    
    @staticmethod
    def get_user_profile(user_id):
        cache_key = f'profile_{user_id}'
        profile = cache.get(cache_key)
        if not profile:
            profile = UserProfile.objects.filter(user_id=user_id).first()
            if profile:
                cache.set(cache_key, profile, 3600)
        return profile
    
    @staticmethod
    def get_user_preferences(user_id):
        cache_key = f'preferences_{user_id}'
        preferences = cache.get(cache_key)
        if not preferences:
            preferences = UserPreference.objects.filter(user_id=user_id).first()
            if preferences:
                cache.set(cache_key, preferences, 3600)
        return preferences
    
    @staticmethod
    @transaction.atomic
    def create_user(email, password, first_name, last_name, phone_number=None, address=None):
        user = User.objects.create_user(email=email, password=password)
        
        UserProfile.objects.create(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number or '',
            address=address or ''
        )
        
        UserPreference.objects.create(
            user_id=user.id
        )
        
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
    def update_user_profile(user_id, **kwargs):
        profile = UserProfile.objects.get(user_id=user_id)
        for key, value in kwargs.items():
            setattr(profile, key, value)
        profile.save()

        cache.delete(f'profile_{user_id}')
        return profile
    
    @staticmethod
    def update_user_preferences(user_id, **kwargs):
        preferences = UserPreference.objects.get(user_id=user_id)
        for key, value in kwargs.items():
            setattr(preferences, key, value)
        preferences.save()

        cache.delete(f'preferences_{user_id}')
        return preferences