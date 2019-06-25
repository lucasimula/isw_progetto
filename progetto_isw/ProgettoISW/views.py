from django.shortcuts import render, redirect
from .forms import *
# Create your views here.


def registrazione(request):
    if request.method == "POST":
        # Assegnamento a registrazioneF il form RegistratiForm
        registrazioneF = FormRegistrazione(request.POST)
        if registrazioneF.is_valid():
            # Se non ci sono errori nel form si creano variabili per contenere i dati inseriti
            nome = registrazioneF.cleaned_data['nome']
            cognome = registrazioneF.cleaned_data['cognome']
            email = registrazioneF.cleaned_data['email']
            citta = registrazioneF.cleaned_data['citta']
            indirizzo = registrazioneF.cleaned_data['indirizzo']
            username = registrazioneF.cleaned_data['username']
            password = registrazioneF.cleaned_data['password']
            confermaPassword = registrazioneF.cleaned_data['confermaPassword']

            # Si crea l'albergatore
            nuovoAlbergatore = Albergatore(nome=str(nome), cognome=str(cognome),
                                           email=str(email), username=str(username),
                                           password=str(confermaPassword), citta=str(citta),
                                           indirizzo=str(indirizzo))
            nuovoAlbergatore.save()
            # Viene salvato l'username come variabile di sessione
            request.session['nomeAlbergatore'] = username
            # L'albergatore appena creato è indirizzato alla sua homepage
            return redirect('/homeAlbergatore/')
    else:
        registrazioneF = FormRegistrazione()
    return render(request, "registrazione.html/", {"form": registrazioneF})


def login(request):
    if request.method == "POST":
        # Assegnamento a loginForm il form LoginForm
        loginF = FormLogin(request.POST)
        # Si controlla se il form ha generato errori
        if loginF.is_valid():
            # Si assegna a una variabile username il valore dell'username messo nel form
            username = loginF.cleaned_data['username']
            # Si controlla se esiste un albergatore con quel username
            if Albergatore.objects.filter(username=username).exists():
                # Se esiste viene settato il suo nome come variabile di sessione
                request.session['nomeAlbergatore'] = username

                return redirect('/homeAlbergatore/')
    else:
        # Se il form non contiene niente
        loginF = FormLogin()
    return render(request, "login.html", {"form": loginF})


def logout(request):
    if 'nomeAlbergatore' in request.session:
        del request.session['nomeAlbergatore']

    if 'idHotel' in request.session:
        del request.session['idHotel']

    return redirect("/home/")


def home(request):
    if 'nomeAlbergatore' in request.session:
        return redirect('/homeAlbergatore/')

    return render(request, "home.html", {'hotel': Hotel.objects.all()})


def homeAlbergatore(request):
    albergatore = ""

    if 'nomeAlbergatore' in request.session:
        albergatore = request.session['nomeAlbergatore']
    else:
        return redirect('/home/')

    elencoPrenotazioni = []
    for p in Prenotazione.objects.all():
        if p.camera.hotel.albergatore.username == albergatore:
            elencoPrenotazioni.append(p)

    return render(request, "homeAlbergatore.html", {'prenotazioni': elencoPrenotazioni})


def listaHotel(request):
    albergatore = ""

    if 'nomeAlbergatore' in request.session:
        albergatore = request.session['nomeAlbergatore']
    else:
        return redirect('/home/')

    elencoHotel = []

    for h in Hotel.objects.all():
        if h.albergatore.username == albergatore:
            elencoHotel.append(h)

    return render(request, "listaHotel.html", {'hotel': elencoHotel})


def aggiungiHotel(request):
    if request.method == 'POST':
        form = FormAggiungiHotel(request.POST)

        if(form.is_valid()):
            username = request.session['nomeAlbergatore']
            nome = form.cleaned_data['nome']
            descrizione = form.cleaned_data['descrizione']
            citta = form.cleaned_data['citta']
            indirizzo = form.cleaned_data['indirizzo']

            for a in Albergatore.objects.all():
                if a.username == str(username):
                    albergatoreFK = a
                    hotel = Hotel(albergatore=albergatoreFK, nome=str(nome),
                                  descrizione=str(descrizione), citta=str(citta), indirizzo=str(indirizzo))
                    hotel.save()
                    return redirect('/listaHotel/')

    else:
        form = FormAggiungiHotel()
        return render(request, 'aggiungiHotel.html', {'form': form})


def gestioneHotel(request):
    hotel = None
    idHotel = request.GET.get('id', None)

    if idHotel is not None:
        hotel = Hotel.objects.get(pk=idHotel)
    else:
        if request.session['idHotel']:
            idHotel = request.session['idHotel']
            hotel = Hotel.objects.get(pk=idHotel)

    if hotel is not None:
        request.session['idHotel'] = idHotel

        elencoCamere = []

        for c in Camera.objects.all():
            if c.hotel == hotel:
                elencoCamere.append(c)

        return render(request, 'gestioneHotel.html', {'hotel': hotel, 'camere': elencoCamere})

    else:
        return redirect('/home/')


def aggiungiCamera(request):
    if request.method == 'POST':
        form = FormAggiungiCamera(request.POST)

        if(form.is_valid()):
            idHotel = request.session['idHotel']
            numero = form.cleaned_data['numero']
            nLetti = form.cleaned_data['nLetti']
            prezzo = form.cleaned_data['prezzo']
            servizi = form.cleaned_data['servizi']

            hotel = Hotel(id=idHotel)

            for h in Hotel.objects.all():
                if h.id == int(idHotel):
                    hotelFK = h
                    camera = Camera(hotel=hotelFK, numero=int(numero),
                                   nLetti=int(nLetti), prezzo=float(prezzo), servizi=str(servizi))
                    camera.save()
                    return redirect('/gestioneHotel/', id=idHotel)

    else:
        hotel = Hotel(id=request.GET.get('id', None))
        form = FormAggiungiCamera()
        return render(request, 'aggiungiCamera.html', {'form': form, 'id': hotel.id})