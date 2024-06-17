from django.urls import path
from .views import home, user_availability, user_profile, edit_profile, create_member, generate_weekly_schedule
from django.conf import settings
from django.conf.urls.static import static

#Nurodome marsrutus ir puslapius
urlpatterns = [
    path('', home, name='home'),  # URL for the home page
    path('home/<str:week>/', home, name='home_with_week'),  # URL for the home page with week parameter
    path('schedule/', user_availability, name='user_availability'),  # URL for user availability page
    path('schedule/<str:schedule_format>/', user_availability, name='user_availability_format'),  # URL for user availability with format
    path('schedule/<str:schedule_format>/<str:week>/', user_availability, name='user_availability_format_with_week'),  # URL for user availability with format and week parameter
    path('schedule/<str:schedule_format>/<str:month>/', user_availability, name='user_availability_format_with_month'),
    path('schedule/<str:schedule_format>/<str:day>/', user_availability, name='user_availability_format_with_day'),
    path('profile/<str:user_id>/', user_profile, name='user_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('create-member/', create_member, name='create_member'),
    path('generate-weekly-schedule/', generate_weekly_schedule, name='generate_weekly_schedule'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)