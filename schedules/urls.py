from django.urls import path
from .views import home, user_availability

#Nurodome marsrutus ir puslapius
urlpatterns = [
    path('', home, name='home'),
    path('schedule/<str:schedule_format>/', user_availability, name='user_availability'), #Marsrutas, puslapis in views (importuojame), pavadinimas (jei noresime kurti pvz. mygtukus, kurie nukreipia i sita puslapi)
]