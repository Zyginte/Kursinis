# Generated by Django 5.0.6 on 2024-06-17 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availability',
            name='is_available',
        ),
        migrations.DeleteModel(
            name='AvailableTime',
        ),
    ]