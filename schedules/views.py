from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from schedules.models import Availability, Vacation, CustomUser
from django.utils import timezone
from datetime import timedelta, datetime

# Create your views here.

def home(request, week=None):
    if week:
        start_date = datetime.strptime(week, '%Y-%m-%d').date() # 
    else:
        today = datetime.now().date() #GETS THE CURRENT DATE
        start_date = today - timedelta(days=today.weekday())  # timedelta(days=today.weekday()) SURANDA KIEK DIENU NUO PIRMADIENIO SIANDIENA YRA | today - timedelta(days=today.weekday()) IS SIANDIENOS DATOS ATIMAMA KIEK DIENU NUO PIRMADIENIO SUSKAICIAVOME IR GAUNAME PIRMADIENIO DATA

    previous_week_start = start_date - timedelta(days=7) # IS PASIRINKTO PIRMADIENIO ATIMA 7 DIENAS, KAD GAUTU PRIES TAI BUVUSIO PIRMADIENIO DATA
    next_week_start = start_date + timedelta(days=7) # PRIE PASIRINKTO PIRMADIENIO PRIDEDA 7 DIENAS, KAD GAUTU ATEINANCIO PIRMADIENIO DATA
    
    date_range = [start_date + timedelta(days=i) for i in range(7)] # SUKURIA SARASA DATU: PRIE PIRMADIENIO DATOS PRIDEDA ATITINKAMA SKAICIU DIENU, KURIAS GAUNAM ITERUOJANT range(7). [start_date + timedelta(days=0) for i in range(0-6)], [start_date + timedelta(days=1) for i in range(0-6)]...
    
    users = CustomUser.objects.all()
    
    data = {
        'users': users,
        'date_range': date_range,
        'previous_week': previous_week_start.strftime('%Y-%m-%d'),  # Convert to string
        'next_week': next_week_start.strftime('%Y-%m-%d'),  # Convert to string
    }
    return render(request, 'home.html', context=data)

def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user.html', {'user': user})


def user_availability(request, schedule_format='week'):
    today = timezone.now().date()

    if schedule_format == 'day':
        start_date = today
        end_date = today
        date_range = [start_date]
    elif schedule_format == 'week':
        start_date = today - timedelta(days=today.weekday())  # Monday
        end_date = start_date + timedelta(days=6)  # Sunday
        date_range = [start_date + timedelta(days=i) for i in range(7)]
    elif schedule_format == 'month':
        start_date = today.replace(day=1)  # First day of the month
        next_month = start_date.month % 12 + 1
        end_date = start_date.replace(month=next_month, day=1) - timedelta(days=1)  # Last day of the month
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    else:
        return HttpResponse("Invalid schedule format", status=400)

    users = CustomUser.objects.all()
    availabilities = Availability.objects.filter(day__range=[start_date, end_date])
    user_vacations = Vacation.objects.filter(first_day__lte=end_date, last_day__gte=start_date)

    vacation_map = {vacation.user_id: vacation for vacation in user_vacations}

    availability_map = {}
    for availability in availabilities:
        if availability.user_id not in availability_map:
            availability_map[availability.user_id] = []
        availability_map[availability.user_id].append(availability)

    users_on_vacation = []
    available_users = []
    not_available_users = []

    for user in users:
        user_available_days = []
        user_vacation_days = []
        for day in date_range:
            if user.id in availability_map:
                for availability in availability_map[user.id]:
                    if availability.day == day:
                        user_available_days.append({
                            'day': day,
                            'available_from': availability.start_time,
                            'available_until': availability.end_time,
                        })
            elif user.id in vacation_map and vacation_map[user.id].first_day <= day <= vacation_map[user.id].last_day:
                user_vacation_days.append({
                    'day': day,
                    'type': vacation_map[user.id].get_type_display(),
                })
        
        if user_available_days:
            available_users.append({
                'user': user,
                'available_days': user_available_days,
            })
        elif user_vacation_days:
            users_on_vacation.append({
                'user': user,
                'vacation_days': user_vacation_days,
            })
        else:
            not_available_users.append({
                'user': user,
            })

    data = {
        'available_users': available_users,
        'not_available_users': not_available_users,
        'users_on_vacation': users_on_vacation,
        'date_range': date_range,
        'hours_range': range(24)
    }

    return render(request, 'schedule.html', context=data)