from django import forms
from django.contrib import admin
from schedules.models import CustomUser, Vacation, Availability
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'name', 'last_name', 'position', 'working_hours', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'last_name', 'position', 'working_hours')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'last_name', 'position', 'working_hours', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name', 'last_name')
    ordering = ('email',)

#----------VACATION
class UsersVacationInline(admin.TabularInline):
    model = Vacation
    extra = 0
    can_delete = False
    readonly_fields = ('first_day', 'last_day', 'type')

class VacationAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_day', 'last_day', 'type')
    list_filter = ('user', 'first_day', 'last_day', 'type')
    search_fields = ('user', 'first_day', 'last_day', 'type')

#----------AVAILABILITY
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['user', 'day', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
class UsersAvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 0
    can_delete = False
    readonly_fields = ('day', 'start_time', 'end_time')


class AvailabilityAdmin(admin.ModelAdmin):
    form = AvailabilityForm
    list_display = ('user', 'day', 'start_time', 'end_time')



# admin.site.register(User)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vacation, VacationAdmin)
admin.site.register(Availability, AvailabilityAdmin)

# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('name', 'last_name', 'email', 'password', 'position', 'working_hours')
#     list_filter = ('name', 'last_name', 'email', 'position', 'working_hours')
#     search_fields = ('name', 'last_name', 'email', 'position', 'working_hours')
#     inlines = [UsersAvailabilityInline, UsersVacationInline]
