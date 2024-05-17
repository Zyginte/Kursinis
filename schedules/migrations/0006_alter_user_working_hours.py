# Generated by Django 5.0.6 on 2024-05-15 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0005_alter_availability_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='working_hours',
            field=models.CharField(choices=[('1', '1 (160h/month)'), ('0.75', '0.75 (120h/month)'), ('0.5', '0.5 (80h/month)'), ('0.25', '0.25 (40h/month)')], default='1', max_length=4, verbose_name='Working hours'),
        ),
    ]
