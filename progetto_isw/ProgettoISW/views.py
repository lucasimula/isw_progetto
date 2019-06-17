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


def aggiungiHotel(request):
    if request.method == 'POST':
        form = FormAggiungiHotel(request.POST)

        if(form.is_valid()):
            nome = form.cleaned_data['nome']
            descrizione = form.cleaned_data['descrizione']
            citta = form.cleaned_data['citta']
            indirizzo = form.cleaned_data['indirizzo']

            hotel = Hotel(nome, descrizione, citta, indirizzo)
            hotel.save()

    else:
        form = FormAggiungiHotel()
        return render(request, 'aggiungiHotel.html', {'form', form})


def gestioneHotel(request):
    return render(request, 'gestioneHotel.html')


def aggiungiCamera(request):
    return render(request, 'aggiungiCamera.html')