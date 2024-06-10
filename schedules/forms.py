from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'last_name', 'position', 'working_hours', 'phone_number', 'profile_picture', 'street_address', 'city', 'postal_code', 'country')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'last_name', 'position', 'working_hours', 'profile_picture', 'phone_number', 'street_address', 'city', 'postal_code', 'country')