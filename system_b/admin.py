from django.contrib import admin
from .models import UserPreference

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'theme', 'language', 'notifications_enabled')
    list_filter = ('theme', 'language', 'notifications_enabled')
    search_fields = ('user_id', 'theme', 'language')
