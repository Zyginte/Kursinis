from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from schedules.models import Availability, Vacation, CustomUser
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm, CustomUserCreationForm
import calendar
import logging

# Create your views here.

#----------------HOME----------------#
def home(request, week=None):
    if week:
        start_date = datetime.strptime(week, '%Y-%m-%d').date() # 
    else:
        today = datetime.now().date() #GETS THE CURRENT DATE
        start_date = today - timedelta(days=today.weekday())  # timedelta(days=today.weekday()) SURANDA KIEK DIENU NUO PIRMADIENIO SIANDIENA YRA | today - timedelta(days=today.weekday()) IS SIANDIENOS DATOS ATIMAMA KIEK DIENU NUO PIRMADIENIO SUSKAICIAVOME IR GAUNAME PIRMADIENIO DATA

    end_date = start_date + timedelta(days=6)

    previous_week_start = start_date - timedelta(days=7) # IS PASIRINKTO PIRMADIENIO ATIMA 7 DIENAS, KAD GAUTU PRIES TAI BUVUSIO PIRMADIENIO DATA
    next_week_start = start_date + timedelta(days=7) # PRIE PASIRINKTO PIRMADIENIO PRIDEDA 7 DIENAS, KAD GAUTU ATEINANCIO PIRMADIENIO DATA
    
    date_range = [start_date + timedelta(days=i) for i in range(7)] # SUKURIA SARASA DATU: PRIE PIRMADIENIO DATOS PRIDEDA ATITINKAMA SKAICIU DIENU, KURIAS GAUNAM ITERUOJANT range(7). [start_date + timedelta(days=0) for i in range(0-6)], [start_date + timedelta(days=1) for i in range(0-6)]...
    
    users = CustomUser.objects.all()
    
    data = {
        'users': users,
        'date_range': date_range,
        'start_date': start_date,
        'end_date': end_date,
        'previous_week': previous_week_start.strftime('%Y-%m-%d'),  # Convert to string
        'next_week': next_week_start.strftime('%Y-%m-%d'),  # Convert to string
    }

    if 'create_member' in request.GET:
        data['create_member'] = True

    return render(request, 'home.html', context=data)

#----------------USER----------------#
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_vacation = Vacation.objects.filter(user=user)
    data = {
        'user': user,
        'user_vacation': user_vacation,
    }
    return render(request, 'profile.html', context=data)

logger = logging.getLogger(__name__)

@login_required
def edit_profile(request):
    logger.debug(f"Initial user: {request.user}")

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            logger.debug(f"Profile updated for user: {request.user}")
            return redirect('user_profile', user_id=request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
            logger.debug(f"Form errors: {form.errors}")

    else:
        form = CustomUserChangeForm(instance=request.user)

    logger.debug(f"Rendering edit_profile with form: {form}")
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def create_member(request):
    logger.debug(f"User creating new member: {request.user}")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password1"])
            new_user.save()
            messages.success(request, 'New team member added.')
            logger.debug(f"New team member created: {new_user}")
            return redirect('user_profile', user_id=request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
            logger.debug(f"Form errors: {form.errors}")
    else:
        form = CustomUserCreationForm()

    logger.debug(f"Rendering create_member with form: {form}")
    return render(request, 'create_member.html', {'form': form})

#----------------AVAILABILITY----------------#
def user_availability(request, schedule_format='week', day=None, week=None, month=None):
    today = timezone.now().date()

    if week:
        start_date = datetime.strptime(week, '%Y-%m-%d').date()
    elif month:
        start_date = datetime.strptime(month, '%Y-%m-%d').date().replace(day=1)
    elif day:
        start_date = datetime.strptime(day, '%Y-%m-%d').date()   
    else:
        start_date = today - timedelta(days=today.weekday())  # Monday

    if schedule_format == 'day':
        start_date = start_date
        end_date = today
        date_range = [start_date]
    elif schedule_format == 'week':
        end_date = start_date + timedelta(days=6)
        date_range = [start_date + timedelta(days=i) for i in range(7)]
    elif schedule_format == 'month':
        end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])  # Last day of the month
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    else:
        return HttpResponse("Invalid schedule format", status=400)
    
    previous_day = start_date - timedelta(days=1)
    next_day = start_date + timedelta(days=1)

    previous_week_start = start_date - timedelta(days=7)
    next_week_start = start_date + timedelta(days=7)

    previous_month_start = (start_date - timedelta(days=start_date.day)).replace(day=1)
    next_month_start = (start_date + timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1])).replace(day=1)

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
            if user.id in vacation_map and vacation_map[user.id].first_day <= day <= vacation_map[user.id].last_day:
                user_vacation_days.append({
                    'day': day,
                    'type': vacation_map[user.id].get_type_display(),
                })

        if user_available_days:
            available_users.append({
                'user': user,
                'available_days': user_available_days,
            })
        else:
            if user_vacation_days:
                vacation = vacation_map[user.id]
                not_available_users.append({
                    'user': user,
                    'on_vacation_from': vacation.first_day,
                    'on_vacation_until': vacation.last_day,
                })
            else:
                not_available_users.append({
                    'user': user,
                    'on_vacation_from': None,
                    'on_vacation_until': None,
                })

    data = {
        'users': users,
        'available_users': available_users,
        'today': today,
        'not_available_users': not_available_users,
        'start_date': start_date,
        'end_date': end_date,
        'date_range': date_range,
        'hours_range': range(24),
        'schedule_format': schedule_format,
        'previous_day': previous_day,
        'next_day': next_day,
        'previous_week': previous_week_start.strftime('%Y-%m-%d'),
        'next_week': next_week_start.strftime('%Y-%m-%d'),
        'previous_month': previous_month_start.strftime('%Y-%m-%d'),
        'next_month': next_month_start.strftime('%Y-%m-%d'),
    }

    return render(request, 'schedule.html', context=data)

def generate_weekly_schedule(request):
    if request.method == 'POST' and request.user.is_superuser:
        generate_schedule()
        return redirect('user_availability_format', schedule_format='week')
    return redirect('user_availability_format', schedule_format='week')