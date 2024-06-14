from django.utils import timezone
from .models import CustomUser, Availability
from datetime import timedelta, datetime
import calendar

def generate_schedule():
    users = CustomUser.objects.all()
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=6)

    for user in users:
        user.schedule = {}
        for day in range(7):
            date = start_date + timedelta(days=day)
            availability = Availability.objects.filter(user=user, date=date).first()
            if availability and availability.is_available:
                user.schedule[date] = "7 am - 2:30 pm"  # Example work hours
            else:
                user.schedule[date] = ""  # Unavailable

        # Save or update the user's schedule in the database

def get_schedule_for_day(user, date):
    availability = Availability.objects.filter(user=user, day=date).first()
    if availability and availability.is_available:
        return f"{availability.start_time} - {availability.end_time}" if availability.start_time and availability.end_time else "7 am - 2:30 pm"  # Example work hours if time is not specified
    return ""

def get_schedule_for_month(user, start_date):
    end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
    schedule = {}
    for day in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=day)
        schedule[date] = get_schedule_for_day(user, date)
    return schedule