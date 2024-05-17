from django.shortcuts import render
from django.http import HttpResponse
from schedules.models import User
import datetime

# Create your views here.

def home(request):
    users = User.objects.all()
    data = {
        'users': users,
    }
    return render(request, 'home.html', context=data)

def schedule_view(request):
    users = User.objects.all()
    current_date = datetime.date.today()  # Get the current date

    context = {
        'users': users,
        'current_date': current_date,
    }
    return render(request, 'schedule.html', context)