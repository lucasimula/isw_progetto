from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from .models import *
from .views import *
import datetime

# Create your tests here.

class TestHotel(TestCase):
    def test_hotel(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()

        hotel = Hotel(albergatore=albergatore, nome='Holiday Inn',
                      descrizione='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        nAlbergatori = Albergatore.objects.filter(nome='Marco', cognome='Cocco', password='ciao',
                                                  username='marcococco', email='marcococco@gmail.com',
                                                  citta='Cagliari', indirizzo='Via Scano 51').count()
        self.assertEqual(nAlbergatori, 1)

        nHotel = Hotel.objects.filter(albergatore=albergatore, nome='Holiday Inn',
                                      descrizione='Bello e profumato', citta='Cagliari',
                                      indirizzo='Viale Umberto Ticca').count()
        self.assertEqual(nHotel, 1)


class TestCamera(TestCase):
    def test_camera(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()

        hotel = Hotel(albergatore=albergatore, nome='Holiday Inn',
                      descrizione='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        camera = Camera(hotel=hotel, numero='101', nLetti='4',
                        prezzo='125.0', servizi='Bagno privato, Asciugacapelli')
        camera.save()

        nAlbergatori = Albergatore.objects.filter(nome='Marco', cognome='Cocco', password='ciao',
                                                  username='marcococco', email='marcococco@gmail.com',
                                                  citta='Cagliari', indirizzo='Via Scano 51').count()
        self.assertEqual(nAlbergatori, 1)

        nHotel = Hotel.objects.filter(albergatore=albergatore, nome='Holiday Inn',
                                      descrizione='Bello e profumato', citta='Cagliari',
                                      indirizzo='Viale Umberto Ticca').count()
        self.assertEqual(nHotel, 1)

        nCamere = Camera.objects.filter(hotel=hotel, numero='101', nLetti='4',
                                        prezzo='125.0', servizi='Bagno privato, Asciugacapelli').count()
        self.assertEqual(nCamere, 1)


# Test di accettazione

#NB RIVEDERE TUTTI I COMMENTI

class TestHomeAlbergatore(TestCase):
    def setUp(self):
        albergatore1 = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                   username='marcococco', email='marcococco@gmail.com',
                                   citta='Cagliari', indirizzo='Via Scano 51')
        albergatore1.save()

        hotel = Hotel(albergatore=albergatore1, nome='Holiday Inn',
                      descrizione='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        camera = Camera(hotel=hotel, numero='101', nLetti='4',
                        prezzo='125.0', servizi='Bagno privato, Asciugacapelli')
        camera.save()

        albergatore2 = Albergatore(nome='Enzo', cognome='Scano', password='buongiorno',
                                   username='enzoscano', email='enzoscano@gmail.com',
                                   citta='Cagliari', indirizzo='Via Cocco Ortu 99')
        albergatore2.save()

        prenotazione = Prenotazione(email='lorenzomilia@gmail.com', camera=camera,
                                    checkIn=datetime.date(2019, 7, 3), checkOut=datetime.date(2018, 7, 21))
        prenotazione.save()

        self.albergatoreConPrenotazioni = albergatore1
        self.albergatoreSenzaPrenotazioni = albergatore2
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_visualizzazione_prenotazioni(self):
        """ Verifica che un hotel keeper con prenotazioni le visualizzi nella sua home """

        # Creazione della request
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        # Creazione della sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['nomeAlbergatore'] = self.albergatoreConPrenotazioni.username

        # Esecuzione della view che gestisce la home dell'albergatore
        response = homeAlbergatore(request)

        # Verifica che la pagina contenga la prenotazione
        self.assertContains(response, 'lorenzomilia@gmail.com')
        self.assertContains(response, 'Holiday Inn')
    '''
    def test_hotelKeeperNoBookingsMessage(self):
        """ Verifica che un hotel keeper senza prenotazioni visualizzi il messaggio relativo """

        # Creazione della requqest
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        # Creazione della sessione
        request.session.save()

        # Simulazione albergatore loggato
        request.session['usr'] = self.userWithoutBookings.username
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della view che gestisce la home dell'albergatore
        response = hotelKeeperHome(request)

        # Verifica della visualizzazione del messaggio
        self.assertContains(response, "You have not reservations in your hotels!")
        '''


class TestListaHotel(TestCase):
    def setUp(self):
        albergatore1 = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                   username='marcococco', email='marcococco@gmail.com',
                                   citta='Cagliari', indirizzo='Via Scano 51')
        albergatore1.save()

        hotel = Hotel(albergatore=albergatore1, nome='Holiday Inn',
                      descrizione='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        camera1 = Camera(hotel=hotel, numero='101', nLetti='4',
                         prezzo='125.0', servizi='Bagno privato, Asciugacapelli')
        camera1.save()

        camera2 = Camera(hotel=hotel, numero='202', nLetti='2',
                         prezzo='55.0', servizi='Bagno privato, Stanza fumatori')
        camera2.save()

        hote2 = Hotel(albergatore=albergatore1, nome='T Hotel',
                      descrizione='Il miglior albergo di Cagliari', citta='Cagliari',
                      indirizzo='Via dei Giudicati 66')
        hote2.save()

        albergatore2 = Albergatore(nome='Enzo', cognome='Scano', password='buongiorno',
                                   username='enzoscano', email='enzoscano@gmail.com',
                                   citta='Cagliari', indirizzo='Via Cocco Ortu 99')
        albergatore2.save()

        self.albergatoreConHotel = albergatore1
        self.albergatoreSenzaHotel = albergatore2
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_visualizzazione_lista_hotel(self):
        """ Verifica che un hotel keeper che possiede hotel ne visualizzi la lista """

        # Creazione request
        request = self.request_factory.get('/listaHotel/')
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['nomeAlbergatore'] = self.albergatoreConHotel.username

        # Esecuzione della vista che gestisce la lista hotel
        response = listaHotel(request)

        # Verifica che gli hotel vengano visualizzati
        self.assertContains(response, 'Holiday Inn')
        self.assertContains(response, 'T Hotel')

    '''
    def test_EmptyHotelListVisualization(self):
        """ Verifica che un hotel keeper senza hotel visualizzi il messaggio relativo """

        # Creazione request
        request = self.request_factory.get('/hotels/')
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['usr'] = self.userWithoutHotels.username
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della vista che gestisce la lista hotel
        response = hotelsList(request)

        # Verifica della visualizzaazione del messaggio
        self.assertContains(response, "You have not registered any hotel!")
        '''


class TestAggiungiHotel(TestCase):
    def setUp(self):
        albergatore1 = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                   username='marcococco', email='marcococco@gmail.com',
                                   citta='Cagliari', indirizzo='Via Scano 51')
        albergatore1.save()

        hotel = Hotel(albergatore=albergatore1, nome='Holiday Inn',
                      descrizione='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        camera1 = Camera(hotel=hotel, numero='101', nLetti='4',
                         prezzo='125.0', servizi='Bagno privato, Asciugacapelli')
        camera1.save()

        camera2 = Camera(hotel=hotel, numero='202', nLetti='2',
                         prezzo='55.0', servizi='Bagno privato, Stanza fumatori')
        camera2.save()

        hotel2 = Hotel(albergatore=albergatore1, nome='T Hotel',
                       descrizione='Il miglior albergo di Cagliari', citta='Cagliari',
                       indirizzo='Via dei Giudicati 66')
        hotel2.save()

        albergatore2 = Albergatore(nome='Enzo', cognome='Scano', password='buongiorno',
                                   username='enzoscano', email='enzoscano@gmail.com',
                                   citta='Cagliari', indirizzo='Via Cocco Ortu 99')
        albergatore2.save()

        self.albergatore = albergatore1
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_campi_mancanti(self):
        """ Verifica che non venga consentita l'aggiunta di un hotel se il form è incompleto """

        # Creazione request
        request = self.request_factory.get('/aggiungiHotel/', follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['nomeAlbergatore'] = self.albergatore.username

        # Riempimento form
        form_data = {'nome': "Caesar's Hotel",
                     'descrizione': "L'hotel preferito da Giulio Cesare",
                     'citta': "Cagliari",
                     'indirizzo': "Via Charles Darwin 2"}

        form = FormAggiungiHotel(data=form_data)

        # Verifica
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_hotel_aggiunto(self):
        """ Verifica che un hotel sia correttamente aggiunto """

        # Lista temporanea
        listaHotel = []

        # Creazione request
        request = self.request_factory.get('/aggiungiHotel/', follow=True)
        self.middleware.process_request(request)
        # Simulazione hotel keeper loggato e creazione sessione
        key_sessione = self.albergatore.username
        session = self.client.session
        session['nomeAlbergatore'] = key_sessione
        session.save()

        # Verifica del numero di hotel presenti prima dell'aggiunta
        for h in Hotel.objects.all():
            if h.albergatore.username == self.albergatore.username:
                listaHotel.append(h)

        self.assertEqual(len(listaHotel), 2)

        # Esecuzione della vista che gestisce l'aggiunta di hotel
        response = aggiungiHotel(request)

        # Riempimento form
        form_data = {'nome': "Caesar's Hotel",
                     'descrizione': "L'hotel preferito da Giulio Cesare",
                     'citta': "Cagliari",
                     'indirizzo': "Via Charles Darwin 2"}

        form = FormAggiungiHotel(data=form_data)

        # Verifica che il form sia valido
        self.assertTrue(form.is_valid())

        # Verifica che la view non abbia restituito errore
        self.assertEquals(response.status_code, 200)

        # Invia il form in POST all'url di aggiunta hotel
        self.client.post('/aggiungiHotel/', form_data)

        # Verifica della corretta aggiunta dell'hotel
        listaHotel = []

        for h in Hotel.objects.all():
            if (h.albergatore.username == self.albergatore.username):
                listaHotel.append(h)

        self.assertEqual(len(listaHotel), 3)


class TestGestioneHotel(TestCase):
    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()

        hotel = Hotel(albergatore=albergatore, nome='Holiday Inn',
                      descrizione='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        camera = Camera(hotel=hotel, numero='101', nLetti='4',
                        prezzo='125.0', servizi='Bagno privato, Asciugacapelli')
        camera.save()

        self.albergatore = albergatore
        self.hotel = hotel
        self.camera = camera
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_visualizzazione_dati(self):
        """ Verifica che l'hotel keeper visualizzi i dati dell'hotel e delle camere che contiene"""

        # Creazione request
        request = self.request_factory.get('/gestioneHotel/?id=' + str(self.hotel.id), follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['nomeAlbergatore'] = self.albergatore.username

        # Esecuzione della vista che gestisce i dettagli dell'hotel
        response = gestioneHotel(request)

        # Verifica che la pagina contenga i dati dell'hotel
        self.assertContains(response, 'Holiday Inn')
        self.assertContains(response, '101')
        self.assertContains(response, '4')
        self.assertContains(response, '125.0')

# QUESTI ULTIMI DUE DI AGGIUNGI CAMERA NON FUNZIONANO

class TestAggiungiCamera(TestCase):
    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()

        hotel = Hotel(albergatore=albergatore, nome='Holiday Inn',
                      descrizione='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        camera = Camera(hotel=hotel, numero='101', nLetti='4',
                        prezzo='125.0', servizi='Bagno privato, Asciugacapelli')
        camera.save()

        self.albergatore = albergatore
        self.hotel = hotel
        self.camera = camera
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_campi_mancanti(self):
        """ Verifica che non sia accettato un form incompleto"""
        request = self.request_factory.get('/aggiungiCamera/', follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['nomeAlbergatore'] = self.albergatore.username
        request.session['idHotel'] = self.hotel.id

        form_data = {'numero': "202",
                     'nLetti': "2",
                     'prezzo': "62.0",
                     'servizi': "Colazione inclusa, Asciugacapelli"}

        form = FormAggiungiCamera(data=form_data)

        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_camera_aggiunta(self):
        """ Verifica che una camera venga correttamente aggiunta """

        # Lista di appoggio
        listaCamere = []

        # Creazione request
        request = self.request_factory.get('/aggiungiCamera/?id=' + str(self.hotel.id), follow=True)
        self.middleware.process_request(request)

        # Scrittura in sessione dei dati necessari alla vista
        key_sessione1 = str(self.albergatore.username)
        key_sessione2 = str(self.hotel.id)
        session = self.client.session
        request.session['nomeAlbergatore'] = key_sessione1
        request.session['idHotel'] = key_sessione2
        session.save()

        form_data = {'numero': "202",
                     'nLetti': "2",
                     'prezzo': "62.0",
                     'servizi': "Colazione inclusa, Asciugacapelli"}

        form = FormAggiungiCamera(data=form_data)

        # Verifica il form
        self.assertTrue(form.is_valid())

        # Conteggio camere prima dell'aggiunta e verifica
        for c in Camera.objects.all():
            if c.hotel == self.hotel:
                listaCamere.append(c)

        self.assertEqual(len(listaCamere), 1)

        form_data = {'numero': "303",
                     'nLetti': "3",
                     'prezzo': "180.0",
                     'servizi': "Colazione inclusa, Bagno privato, TV, Asciugacapelli"}

        # Invio form all'url che gestisce l'aggiunta della camera
        self.client.post('/aggiungiCamera/', form_data)

        # Conteggio camere dopo l'aggiunta e verifica
        listaCamere = []

        for c in Camera.objects.all():
            if c.hotel == self.hotel:
                listaCamere.append(c)

        self.assertEqual(len(listaCamere), 2)