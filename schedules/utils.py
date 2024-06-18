from django.utils import timezone
from .models import CustomUser, Availability, Vacation
from datetime import timedelta, datetime
import calendar
import logging

logger = logging.getLogger(__name__)

def generate_schedule(week=None):
    users = CustomUser.objects.all()
    start_date = timezone.now().date()

    if week:
        start_date = datetime.strptime(week, '%Y-%m-%d').date()

    users_scheduled_dates_hours = {}

    for user in users:
        user.schedule = {}

        vacations = Vacation.objects.filter(user=user, first_day__lte=start_date + timedelta(days=6), last_day__gte=start_date)

        for day in range(7):
            week_date = start_date + timedelta(days=day)
            current_date_key = week_date
            
            if any(vacation.first_day <= current_date_key <= vacation.last_day for vacation in vacations):
                user.schedule[current_date_key] = "Vacation"
            else:
                availability = Availability.objects.filter(user=user, day=current_date_key).first()

                if availability and availability.start_time and availability.end_time:
                    start_time = datetime.combine(current_date_key, availability.start_time)
                    end_time = datetime.combine(current_date_key, availability.end_time)

                    if current_date_key not in user.schedule:
                        work_hours = f"{start_time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')} - {end_time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')}"
                        user.schedule[current_date_key] = work_hours

        users_scheduled_dates_hours[user.id] = user.schedule

    return users_scheduled_dates_hours

def get_schedule_for_day(user, date):
    availability = Availability.objects.filter(user=user, day=date).first()
    if availability and availability.is_available:
        return f"{availability.start_time} - {availability.end_time}" if availability.start_time and availability.end_time else ""  # Example work hours if time is not specified
    return ""

def get_schedule_for_month(user, start_date):
    end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
    schedule = {}
    for day in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=day)
        schedule[date] = get_schedule_for_day(user, date)
    return schedule