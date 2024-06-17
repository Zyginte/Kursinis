from django.utils import timezone
from .models import CustomUser, Availability, AvailableTime, Vacation
from datetime import timedelta, datetime, time, date
import calendar
from django.db.models import Sum
import logging

logger = logging.getLogger(__name__)

def generate_schedule(week=None):
    users = CustomUser.objects.all()
    start_date = timezone.now()

    if week:
        start_date = datetime.strptime(week, '%Y-%m-%d')

    end_date = start_date + timedelta(days=6)
    user_scheduled_hours = {}

    for user in users:
        user.schedule = {}
        total_scheduled_hours = 0
        monthly_working_hours_limit = float(user.working_hours) * 160

        for day in range(7):
            current_date = start_date + timedelta(days=day)
            current_date_key = current_date.date()
            availability = Availability.objects.filter(user=user, day=current_date_key).first()

            logger.debug(f"User: {user}, Date: {current_date}, Availability: {availability}")

            if availability and availability.start_time and availability.end_time:
                start_time = datetime.combine(current_date_key, availability.start_time)
                end_time = datetime.combine(current_date_key, availability.end_time)
                total_available_hours = (end_time - start_time).total_seconds() / 3600

                if current_date_key not in user.schedule:
                    user.schedule[current_date_key] = []

                for hour in range(int(total_available_hours)):
                    current_hour = start_time + timedelta(hours=hour)

                    if user_scheduled_hours.get(user.id, None):
                        last_scheduled_hour = user_scheduled_hours[user.id][-1]
                        if current_hour - last_scheduled_hour < timedelta(hours=1):
                            continue

                    if len(user.schedule[current_date_key]) < 4:
                        work_hours = f"{current_hour.strftime('%I %p').lstrip('0').replace(' 0', ' ')} - {end_time.strftime('%I %p').lstrip('0').replace(' 0', ' ')}"
                        user.schedule[current_date_key].append(work_hours)
                        total_scheduled_hours += 1
                        user_scheduled_hours.setdefault(user.id, []).append(current_hour)

                        if total_scheduled_hours > monthly_working_hours_limit:
                            excess_hours = total_scheduled_hours - monthly_working_hours_limit
                            excess_hour_time = start_time + timedelta(hours=hour - excess_hours)
                            user.schedule[current_date_key].pop()
                            total_scheduled_hours -= 1

    return {user.id: user.schedule for user in users}

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