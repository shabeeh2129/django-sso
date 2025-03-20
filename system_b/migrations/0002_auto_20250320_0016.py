# Generated by Django 3.2.24 on 2025-03-20 00:16

from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('system_b', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreference',
            name='dashboard_layout',
            field=djongo.models.fields.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='notification_preferences',
            field=djongo.models.fields.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='work_hours',
            field=djongo.models.fields.JSONField(default=dict),
        ),
    ]
