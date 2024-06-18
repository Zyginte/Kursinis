from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from schedules.models import Availability, Vacation, CustomUser, Schedule
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm, CustomUserCreationForm
import calendar
import logging
from .utils import generate_schedule, get_schedule_for_day, get_schedule_for_month

# Create your views here.
logger = logging.getLogger(__name__)

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

    schedule_data = []
    for user in users:
        user_schedule = Schedule.objects.filter(user=user, date__range=[start_date, end_date]).order_by('date')
        schedule_row = {'user': user, 'schedule': []}
        for day in date_range:
            work_hours = user_schedule.filter(date=day).first()
            if work_hours:
                schedule_row['schedule'].append(work_hours.hours)
            else:
                schedule_row['schedule'].append("")
        schedule_data.append(schedule_row)
    
    data = {
        'users': users,
        'date_range': date_range,
        'start_date': start_date,
        'end_date': end_date,
        'previous_week': previous_week_start.strftime('%Y-%m-%d'),
        'next_week': next_week_start.strftime('%Y-%m-%d'),
        'schedule_data': schedule_data,
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
            return redirect('user_profile', user_id=new_user.id)
        else:
            # Capture form errors and log them
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(f"Error in {field}: {error}")
            messages.error(request, 'Please correct the error(s) below.')
            logger.debug(f"Form errors: {form.errors}")
    else:
        form = CustomUserCreationForm()

    logger.debug(f"Rendering create_member with form: {form}")
    return render(request, 'create_member.html', {'form': form})

#----------------AVAILABILITY + SCHEDULE----------------#
def user_availability(request, schedule_format='week', day=None, week=None, month=None):
    today = timezone.now()

    if week:
        start_date = datetime.strptime(week, '%Y-%m-%d')
    elif month:
        start_date = datetime.strptime(month, '%Y-%m-%d').replace(day=1)
    elif day:
        start_date = datetime.strptime(day, '%Y-%m-%d')
    else:
        start_date = today - timedelta(days=today.weekday())

    if schedule_format == 'day':
        end_date = start_date
        date_range = [start_date]
    elif schedule_format == 'week':
        end_date = start_date + timedelta(days=6)
        date_range = [start_date + timedelta(days=i) for i in range(7)]
    elif schedule_format == 'month':
        end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
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
    available_dates = Availability.objects.filter(day__range=[start_date.date(), end_date.date()])
    user_vacations = Vacation.objects.filter(first_day__lte=end_date.date(), last_day__gte=start_date.date())

    vacation_map = {vacation.user_id: vacation for vacation in user_vacations}

    available_dates_map = {}
    for availability in available_dates:
        if availability.user_id not in available_dates_map:
            available_dates_map[availability.user_id] = []
        available_dates_map[availability.user_id].append(availability)

    available_users = []
    not_available_users = []

    for user in users:
        user_schedule = {}
        for day in date_range:
            availabilities = available_dates_map.get(user.id, [])
            for availability in availabilities:
                if availability.day == day.date():
                    work_hours = f"{availability.start_time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')} - {availability.end_time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')}"
                    user_schedule[day] = work_hours
                    break
            else:
                user_schedule[day] = "No schedule available"

        if user_schedule:
            available_users.append({
                'user': user,
                'schedule': user_schedule,
            })
        else:
            if user.id in vacation_map:
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

    # Fetch the already generated schedule from the database
    generated_schedule = {}
    for schedule in Schedule.objects.filter(date__range=[start_date.date(), end_date.date()]):
        if schedule.user_id not in generated_schedule:
            generated_schedule[schedule.user_id] = {}
        generated_schedule[schedule.user_id][schedule.date] = schedule.hours

    schedule_data = []
    for user_id, schedule in generated_schedule.items():
        user = CustomUser.objects.get(id=user_id)
        if schedule_format == 'week':
            schedule_row = {'user': user, 'schedule': []}
            for day in date_range:
                day_str = day.date().isoformat()
                work_hours = schedule.get(day.date(), "")
                schedule_row['schedule'].append({'date': day_str, 'work_hours': work_hours})
            schedule_data.append(schedule_row)

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
        'generated_schedule': generated_schedule,
        'schedule_data': schedule_data,
    }

    return render(request, 'schedule.html', context=data)

def generate_weekly_schedule(request):
    if request.method == 'POST' and request.user.is_superuser:
        week = request.POST.get('week')
        if week:
            generated_schedule = generate_schedule(week)

            for user_id, schedule in generated_schedule.items():
                for date, hours in schedule.items():
                    Schedule.objects.update_or_create(
                        user_id=user_id,
                        date=date,
                        defaults={'hours': hours}
                    )

            messages.success(request, f"Schedule for the week starting {week} has been generated.")
        else:
            messages.error(request, "No week specified.")
        return redirect('user_availability_format_with_week', schedule_format='week', week=week)
    return redirect('user_availability_format_with_week', schedule_format='week')