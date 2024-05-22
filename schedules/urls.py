from django.urls import path
from .views import home, user_view

#Nurodome marsrutus ir puslapius
urlpatterns = [
    path('', home, name='home'), #Marsrutas, puslapis is views (importuojame), pavadinimas (jei noresime kurti pvz. mygtukus, kurie nukreipia i sita puslapi)
    path('user/', user_view, name='user')
]