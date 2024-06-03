from django.shortcuts import render
from django.http import HttpResponse
from schedules.models import Availability, Vacation, CustomUser
from django.utils import timezone

# Create your views here.

def home(request):
    users = CustomUser.objects.all()
    data = {
        'users': users,
    }
    return render(request, 'home.html', context=data)

def user_availability(request):
    today = timezone.now().date()
    users = CustomUser.objects.all()
    availabilities_today = Availability.objects.filter(day=today)
    user_vacation = Vacation.objects.filter(first_day__lte=today, last_day__gte=today)

    vacation_map = {vacation.user_id: vacation for vacation in user_vacation}

    availability_map = {availability.user_id: availability for availability in availabilities_today}

    users_on_vacation = []
    available_users = []
    not_available_users = []

    for user in users:
        if user.id in availability_map:
            availability = availability_map[user.id]
            available_from = availability.start_time
            available_until = availability.end_time

            available_users.append({
                'user': user,
                'available_from': available_from,
                'available_until': available_until,
            })
        elif user.id in vacation_map:
            on_vacation = vacation_map[user.id]
            on_vacation_from = on_vacation.first_day
            on_vacation_until = on_vacation.last_day

            not_available_users.append({
                'user': user,
                'on_vacation_from': on_vacation_from,
                'on_vacation_until': on_vacation_until,
                'type': on_vacation.get_type_display(),
            })
        else:
            # If neither available nor on vacation, add to not_available_users
            not_available_users.append({
                'user': user,
            })

    data = {
        'available_users': available_users,
        'not_available_users': not_available_users,
        'users_on_vacation': users_on_vacation,
        'today': today,
        'hours_range': range(24)
    }

    return render(request, 'schedule.html', context=data)