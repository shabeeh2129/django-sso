from djongo import models

class UserPreference(models.Model):
    user_id = models.UUIDField(primary_key=True)
    theme = models.CharField(max_length=50, default='light')
    language = models.CharField(max_length=10, default='en')
    notifications_enabled = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'system_b'