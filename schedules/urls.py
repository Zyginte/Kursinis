from django.urls import path
from .views import home, user_availability

#Nurodome marsrutus ir puslapius
urlpatterns = [
    path('', home, name='home'),
    path('schedule/', user_availability, name='schedule'), #Marsrutas, puslapis is views (importuojame), pavadinimas (jei noresime kurti pvz. mygtukus, kurie nukreipia i sita puslapi)
]