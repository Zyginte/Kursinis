from django.urls import path
from .views import home, user_availability, user_profile, edit_profile
from django.conf import settings
from django.conf.urls.static import static

#Nurodome marsrutus ir puslapius
urlpatterns = [
    path('', home, name='home'),  # URL for the home page
    path('home/<str:week>/', home, name='home_with_week'),  # URL for the home page with week parameter
    path('schedule/', user_availability, name='user_availability'),  # URL for user availability page
    path('schedule/<str:schedule_format>/', user_availability, name='user_availability_format'), #Marsrutas, puslapis in views (importuojame), pavadinimas (jei noresime kurti pvz. mygtukus, kurie nukreipia i sita puslapi)
    path('profile/<str:user_id>/', user_profile, name='user_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)