import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.template.defaultfilters import safe
from django.urls import reverse
from .forms import *


def registrazione(request):
    if request.method == "POST":

        registrazioneF = FormRegistrazione(request.POST)        # Assegnamento a registrazioneF il form RegistratiForm
        if registrazioneF.is_valid():            # Se non ci sono errori nel form si creano variabili per contenere i dati inseriti

            nome = registrazioneF.cleaned_data['nome']
            cognome = registrazioneF.cleaned_data['cognome']
            email = registrazioneF.cleaned_data['email']

            username = registrazioneF.cleaned_data['username']
            password = registrazioneF.cleaned_data['password']
            confermaPassword = registrazioneF.cleaned_data['confermaPassword']

            nuovoAlbergatore = Albergatore(nome=str(nome), cognome=str(cognome),            # Si crea l'albergatore
                                           email=str(email), username=str(username),
                                           password=str(confermaPassword))
            nuovoAlbergatore.save()

            request.session['nomeAlbergatore'] = username            # Viene salvato l'username come variabile di sessione

            return redirect('/homeAlbergatore/')            # L'albergatore appena creato è indirizzato alla sua homepage
    else:
        registrazioneF = FormRegistrazione()
    return render(request, "registrazione.html/", {"form": registrazioneF})


def login(request):
    if request.method == "POST":

        loginF = FormLogin(request.POST)        # Assegnamento a loginForm il form LoginForm

        if loginF.is_valid():        # Si controlla se il form ha generato errori

            username = loginF.cleaned_data['username']            # Si assegna a una variabile username il valore dell'username messo nel form

            if Albergatore.objects.filter(username=username).exists():            # Si controlla se esiste un albergatore con quel username

                request.session['nomeAlbergatore'] = username                # Se esiste viene settato il suo nome come variabile di sessione

                return redirect('/homeAlbergatore/')
    else:

        if 'nomeAlbergatore' in request.session:        # Se l'albergatore è già loggato verrà reindirizzato alla sua home
            return redirect("/homeAlbergatore/")
        else:

            loginF = FormLogin()            # Se il form non contiene niente
    return render(request, "login.html", {"form": loginF})


def logout(request):

    if 'nomeAlbergatore' in request.session:    # Se un albergatore è loggato si elimina il nome dalla sessione
        del request.session['nomeAlbergatore']

    if 'idHotel' in request.session:
        del request.session['idHotel']

    return redirect("/home/")


def home(request):

    if 'nomeAlbergatore' in request.session:     # Se un albergatore è loggato si apre la sua home personale
        return redirect('/homeAlbergatore/')

    return redirect('/home/')


def homeAlbergatore(request):

    if 'nomeAlbergatore' in request.session:
        for a in Albergatore.objects.all():
            if a.username == request.session['nomeAlbergatore']:
                albergatore = a
                elencoPrenotazioni = []
                for p in Prenotazione.objects.all():     # Si recuperano le informazioni da visualizzare nella home personale
                    if p.camera.hotel.albergatore.username == albergatore.username:
                        elencoPrenotazioni.append(p)

                return render(request, "homeAlbergatore.html", {'prenotazioni': elencoPrenotazioni})
        return redirect('/home/')
    else:
        return redirect('/home/')


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
    if 'nomeAlbergatore' not in request.session:
        return redirect('/home/')

    if request.method == 'POST':
        form = FormAggiungiHotel(request.POST)

        if form.is_valid():
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
    if 'nomeAlbergatore' not in request.session:
        return redirect('/home/')

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
    if 'nomeAlbergatore' not in request.session:
        return redirect('/home/')

    if request.method == 'POST':
        form = FormAggiungiCamera(request.POST)

        if form.is_valid():
            idHotel = request.session['idHotel']
            numero = form.cleaned_data['numero']
            nLetti = form.cleaned_data['nLetti']
            prezzo = form.cleaned_data['prezzo']
            servizi = form.cleaned_data['servizi']

            hotel = Hotel(id=idHotel)

            for h in Hotel.objects.all():
                if h.id == int(idHotel):
                    hotelFK = h

                    for c in Camera.objects.all():
                        if c.hotel == hotelFK and c.numero == numero:
                            messages.add_message(request, messages.ERROR, 'Esiste già una camera con quel numero.')
                            return render(request, 'aggiungiCamera.html', {'form': form, 'id': hotel.id})

                    camera = Camera(hotel=hotelFK, numero=int(numero),
                                   nLetti=int(nLetti), prezzo=float(prezzo), servizi=str(servizi))
                    camera.save()
                    return redirect('/gestioneHotel/', id=idHotel)

    else:
        hotel = Hotel(id=request.GET.get('id', None))
        form = FormAggiungiCamera()
        return render(request, 'aggiungiCamera.html', {'form': form, 'id': hotel.id})


def cercaB(request):
    request.session.flush();
    return render(request, "cercaB.html", {'form': FormRicerca()})


def cercaRS(request):
    lista = []

    if request.method == 'GET':
        form = FormRicerca(request.GET)
        if form.is_valid():
            cercaCitta = form.cleaned_data['cercaCitta']
            cercaLetti = form.cleaned_data['cercaLetti']
            cercaCheckIn = request.GET.get('cercaCheckIn', None)
            cercaCheckOut = request.GET.get('cercaCheckOut', None)

            if cercaCheckIn != None and cercaCheckOut != None and cercaCitta != None and cercaLetti != None:

                for ca in Camera.objects.all():

                    if ca.hotel.citta == cercaCitta and str(ca.nLetti) == cercaLetti:

                        listIn = cercaCheckIn.split("-")
                        listOut = cercaCheckOut.split("-")

                        checkinDT = datetime.date(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                        checkoutDT = datetime.date(int(listOut[0]), int(listOut[1]), int(listOut[2]))

                        request.session['checkinDT'] = cercaCheckIn
                        request.session['checkoutDT'] = cercaCheckOut

                        dataEsiste = 0

                        for item in Prenotazione.objects.all():
                            if item.camera.id == ca.id:                        # Viene controllato se la data di checIn o checkOut inserita è compresa in quelle prenotate e viceversa

                                if checkinDT >= item.checkIn and checkinDT <= item.checkOut:
                                    dataEsiste = dataEsiste + 1
                                if item.checkIn >= checkinDT and item.checkIn <= checkoutDT:
                                    dataEsiste = dataEsiste + 1
                                if checkoutDT >= item.checkIn and checkoutDT <= item.checkOut:
                                    dataEsiste = dataEsiste + 1
                                if item.checkOut >= checkinDT and item.checkOut <= checkoutDT:
                                    dataEsiste = dataEsiste + 1

                        if dataEsiste > 0:

                            return render(request, "cercaB.html", {'form':FormRicerca(),'lista2': '1'})
                        else:

                            tmp = [ca.hotel.nome, ca.nLetti, ca.prezzo, ca.servizi, ca.id, ca.hotel.citta, ca.numero]

                            if tmp not in lista:
                                lista.append(tmp)

                        if checkoutDT < checkinDT:
                            return render(request, "cercaB.html", {'form':FormRicerca()})

        if len(lista) > 0:
            context = {'lista': lista}
        else:
            context = {'lista2': '1'}

        return render(request, "cercaAl.html", context)


def prenotazione(request):
    if 'checkinDT' not in request.session:
        return render(request, "cercaB.html", {'form': FormRicerca()})
    if request.GET.get('numeroCamera') is None:
        return render(request, "cercaB.html", {'form': FormRicerca()})
    try:
        numeroCamera = request.GET.get('numeroCamera', None)
    except:
        numeroCamera = None

    cameraDaPrenotare = Camera.objects.get(id=numeroCamera)    # Viene utilizzato l'id per distinguere le camere in modo univoco
    lista = []

    tmp = [cameraDaPrenotare.hotel.nome, cameraDaPrenotare.nLetti, cameraDaPrenotare.prezzo, cameraDaPrenotare.servizi, cameraDaPrenotare.id, cameraDaPrenotare.hotel.citta,
           request.session['checkinDT'], cameraDaPrenotare.hotel.indirizzo, request.session['checkoutDT'], cameraDaPrenotare.numero]
    lista.append(tmp)
    context = {'cameraDaPrenotare': lista}
    request.session['idCam'] = numeroCamera
    return render(request, "confermaPrenotazione.html", {'form': FormConferma(), 'cameraDaPrenotare': lista})


def confermaPrenotazione(request):
    if 'checkinDT' not in request.session:
        return render(request, "cercaB.html", {'form': FormRicerca()})

    checkinDT = request.session['checkinDT']
    checkoutDT = request.session['checkoutDT']
    if request.method == 'GET':
        form = FormConferma(request.GET)
        if form.is_valid():
            emailPrenotazione = form.cleaned_data['email']
            if emailPrenotazione != None:
                numeroCamera = request.session['idCam']

            if numeroCamera is not None:
                cameraPrenotata = Camera.objects.get(id=numeroCamera)

                prenot = Prenotazione(email=emailPrenotazione, camera=cameraPrenotata, checkIn=checkinDT, checkOut=checkoutDT)

                prenot.save()
                return redirect('/home/')

    return render(request, "cercaB.html", {'form': FormRicerca()})

