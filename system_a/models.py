import uuid
from django.db import models

class UserProfile(models.Model):
    user_id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    class Meta:
        app_label = 'system_a'