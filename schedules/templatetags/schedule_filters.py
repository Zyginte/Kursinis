from django import template

register = template.Library()

@register.filter
def get_schedule_for_day(schedule, day):
    return schedule.get(day, '')

@register.filter
def get_schedule_for_hour(schedule, hour):
    # Implement the logic for displaying schedule by hour
    hourly_schedule = ""
    for time, details in schedule.items():
        if time.hour == hour:
            hourly_schedule += details + " "
    return hourly_schedule.strip()