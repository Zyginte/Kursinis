from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


#----------CUSTOM USER----------#
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, last_name, position, working_hours, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, last_name=last_name, position=position, working_hours=working_hours, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, last_name, position, working_hours, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, last_name, position, working_hours, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    WORKING_HOURS = (
        ('1', '1 (160h/month)'),
        ('0.75', '0.75 (120h/month)'),
        ('0.5', '0.5 (80h/month)'),
        ('0.25', '0.25 (40h/month)'),
        ('1.25', '1.25 (180h/month)'),
        ('1.5', '1.5 (200h/month)')
    )
    working_hours = models.CharField(max_length=4, choices=WORKING_HOURS, default='1')
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name', 'position', 'working_hours']

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.id)])
    
    def full_address(self):
        return f"{self.street_address}, {self.city}, {self.postal_code}, {self.country}"

    def __str__(self):
        return f'{self.name} {self.last_name}'
    
#----------VACATION----------#
class Vacation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)
    first_day = models.DateField('First day', null=False)
    last_day = models.DateField('Last day', null=False)
    TYPE = (
        ('a', 'Anual leave'),
        ('b', 'Birthday day'),
        ('c', 'Welness day'),
        ('d', 'Bussines trip')
    )
    type = models.CharField('Type of vacation', max_length=1, default='a', choices=TYPE)
    # users = models.ManyToManyField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user} {self.first_day} {self.last_day} {self.type})'


#----------AVAILABILITY----------#
class Availability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day = models.DateField('Day', null=False)
    start_time = models.TimeField('Available from', null=True, blank=True)
    end_time = models.TimeField('Available to', null=True, blank=True)

    class Meta:
        verbose_name = 'Availability'
        verbose_name_plural = 'Availabilities'

    def __str__(self):
        return f'{self.user} - {self.day} - {self.start_time} to {self.end_time}'
    
#----------SCHEDULE----------#
class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user} - {self.date}: {self.hours}"

#python manage.py makemigrations
#python manage.py migrate