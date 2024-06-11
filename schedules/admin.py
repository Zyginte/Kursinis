from django import forms
from django.contrib import admin
from schedules.models import CustomUser, Vacation, Availability
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'name', 'last_name', 'position', 'working_hours', 'phone_number', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password','profile_picture')}),
        ('Personal info', {'fields': ('name', 'last_name', 'position', 'working_hours', 'phone_number', 'street_address', 'city', 'postal_code', 'country')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'last_name', 'position', 'working_hours', 'phone_number', 'street_address', 'city', 'state', 'postal_code', 'country', 'profile_picture', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name', 'last_name')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.set_unusable_password()
        obj.save()

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




admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vacation, VacationAdmin)
admin.site.register(Availability, AvailabilityAdmin)