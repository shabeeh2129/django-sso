from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'last_name', 'phone_number')
    search_fields = ( 'last_name', 'phone_number')
    list_filter = ( 'last_name',)
    ordering = ( 'last_name',)
