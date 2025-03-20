from django.db import models
import uuid
from django.utils import timezone

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        app_label = 'system_a'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100, blank=True)
    join_date = models.DateField(default=timezone.now)

    class Meta:
        app_label = 'system_a'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
