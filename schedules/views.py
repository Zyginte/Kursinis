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

# def user_view(request):
#     users = User.objects.all()

#     context = {
#         'users': users,
#     }
#     return render(request, 'user.html', context=context)

def user_view(request):
    current_user = request.user
    # name = current_user.name
    # last_name = current_user.last_name

    context = {
        'current_user': current_user,
    }
    return render(request, 'user.html', context=context)
