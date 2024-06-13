from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    name = forms.CharField(max_length=30, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.')
    position = forms.CharField(max_length=100, help_text='Enter your position within the team.')
    working_hours = forms.CharField(max_length=100, help_text='Enter your working hours.')
    phone_number = forms.CharField(max_length=30, required=False, help_text='Enter your phone number.')
    profile_picture = forms.ImageField(required=False, help_text='Upload your profile picture.')
    street_address = forms.CharField(max_length=100, required=False, help_text='Enter your street address.')
    city = forms.CharField(max_length=100, required=False, help_text='Enter your city.')
    postal_code = forms.CharField(max_length=20,required=False, help_text='Enter your postal code.')
    country = forms.CharField(max_length=100, required=False, help_text='Enter your country.')
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'name', 'last_name', 'position', 'working_hours', 'phone_number', 'profile_picture', 'street_address', 'city', 'postal_code', 'country')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'last_name', 'position', 'working_hours', 'profile_picture', 'phone_number', 'street_address', 'city', 'postal_code', 'country')