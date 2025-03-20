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

    def get_defaults(self):
        """Return all default values for the model."""
        return {
            'notification_preferences': {
                'email': True,
                'push': True,
                'department_updates': True,
                'task_reminders': True
            },
            'dashboard_layout': {
                'widgets': [
                    {'id': 'tasks', 'position': 1},
                    {'id': 'department_updates', 'position': 2},
                    {'id': 'calendar', 'position': 3}
                ]
            },
            'work_hours': {
                'monday': {'start': '09:00', 'end': '17:00'},
                'tuesday': {'start': '09:00', 'end': '17:00'},
                'wednesday': {'start': '09:00', 'end': '17:00'},
                'thursday': {'start': '09:00', 'end': '17:00'},
                'friday': {'start': '09:00', 'end': '17:00'}
            }
        }

    def save(self, *args, **kwargs):
        defaults = self.get_defaults()
        if not self.notification_preferences:
            self.notification_preferences = defaults['notification_preferences']
        if not self.dashboard_layout:
            self.dashboard_layout = defaults['dashboard_layout']
        if not self.work_hours:
            self.work_hours = defaults['work_hours']
        super().save(*args, **kwargs)