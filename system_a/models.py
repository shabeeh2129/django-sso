from django.db import models
import uuid

class UserProfile(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        app_label = 'system_a'
