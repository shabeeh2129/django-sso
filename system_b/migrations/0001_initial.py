# Generated by Django 3.2 on 2025-03-19 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('user_id', models.UUIDField(primary_key=True, serialize=False)),
                ('theme', models.CharField(default='light', max_length=50)),
                ('language', models.CharField(default='en', max_length=10)),
                ('notifications_enabled', models.BooleanField(default=True)),
            ],
        ),
    ]
