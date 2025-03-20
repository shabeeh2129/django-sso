from djongo import models

class UserPreference(models.Model):
    user_id = models.UUIDField(primary_key=True)
    theme = models.CharField(max_length=50, default='light')
    language = models.CharField(max_length=10, default='en')
    notifications_enabled = models.BooleanField(default=True)
    notification_preferences = models.JSONField(default=dict)  # For storing notification settings
    dashboard_layout = models.JSONField(default=dict)  # For storing dashboard widget positions
    work_hours = models.JSONField(default=dict)  # For storing preferred work hours
    
    class Meta:
        app_label = 'system_b'

    def __str__(self):
        return f"Preferences for user {self.user_id}"

    def get_default_notification_preferences(self):
        return {
            'email': True,
            'push': True,
            'department_updates': True,
            'task_reminders': True
        }

    def get_default_dashboard_layout(self):
        return {
            'widgets': [
                {'id': 'tasks', 'position': 1},
                {'id': 'department_updates', 'position': 2},
                {'id': 'calendar', 'position': 3}
            ]
        }

    def get_default_work_hours(self):
        return {
            'monday': {'start': '09:00', 'end': '17:00'},
            'tuesday': {'start': '09:00', 'end': '17:00'},
            'wednesday': {'start': '09:00', 'end': '17:00'},
            'thursday': {'start': '09:00', 'end': '17:00'},
            'friday': {'start': '09:00', 'end': '17:00'}
        }

    def save(self, *args, **kwargs):
        if not self.notification_preferences:
            self.notification_preferences = self.get_default_notification_preferences()
        if not self.dashboard_layout:
            self.dashboard_layout = self.get_default_dashboard_layout()
        if not self.work_hours:
            self.work_hours = self.get_default_work_hours()
        super().save(*args, **kwargs)