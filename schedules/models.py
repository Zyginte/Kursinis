from django.db import models
from django.db.models import Q

# Create your models here.

class User(models.Model):
    #id
    name = models.CharField('First name', max_length=100)
    last_name = models.CharField('Last name', max_length=100)
    email = models.EmailField('Email', max_length=100)
    password = models.CharField('Password', max_length=100)
    position = models.CharField('Position', max_length=100)
    WORKING_HOURS = (
        ('1', '1 (160h/month)'),
        ('0.75', '0.75 (120h/month)'),
        ('0.5', '0.5 (80h/month)'),
        ('0.25', '0.25 (40h/month)'),
        ('1.25', '1.25 (180h/month)'),
        ('1.5', '1.5 (200h/month)')
    )
    working_hours = models.CharField('Working hours', max_length=4, default='1', choices=WORKING_HOURS)


    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'
    
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f'{self.user.username} Profile'

class Vacation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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

class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    day = models.DateField('Day', null=False)
    start_time = models.TimeField('Available from', null=True, blank=True)
    end_time = models.TimeField('Available to', null=True, blank=True)

    class Meta:
        verbose_name = 'Availability'
        verbose_name_plural = 'Availabilities'
    


#python manage.py makemigrations
#python manage.py migrate