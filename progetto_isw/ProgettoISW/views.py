from django.shortcuts import render
from .models import *

# Create your views here.


def login(request):
    return render(request)


def home(request):
    return render(request, "home.html", {'hotel': Hotel.objects.all()})


def homeAlbergatore(request):
    #albergatore
    elencoPrenotazioni = []

    for p in Prenotazione.objects.all():
        elencoPrenotazioni.append(p)

    return render(request, "homeAlbergatore.html", {'prenotazioni': elencoPrenotazioni})


def listaHotel(request):
    #albergatore
    elencoHotel = []

    for h in Hotel.objects.all():
        elencoHotel.append(p)

    return render(request, "listaHotel.html", {'prenotazioni': elencoHotel})