from django.shortcuts import render
from django.http import HttpResponse
from schedules.models import Schedule, Availability
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    users = User.objects.all()
    data = {
        'users': users,
    }
    return render(request, 'home.html', context=data)

def user_availability(request):
    today = timezone.now().date()
    users = User.objects.all()
    availabilities_today = Availability.objects.filter(day=today)

    availability_map = {availability.user_id: availability for availability in availabilities_today}

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

        else:
            not_available_users.append({
                'user': user,
            })

    data = {
        'available_users': available_users,
        'not_available_users': not_available_users,
        'today': today,
    }

    return render(request, 'schedule.html', context=data)