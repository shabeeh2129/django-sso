from django.contrib import admin
from .models import UserProfile, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'department', 'position', 'join_date')
    list_filter = ('department', 'position')
    search_fields = ('first_name', 'last_name', 'user_id')
    ordering = ('-join_date',)
    readonly_fields = ('user_id', 'join_date')
