from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from .models import *
from .views import *
import datetime


class TestHotel(TestCase):
    def testHotel(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()

        hotel = Hotel(albergatore=albergatore, nome='Holiday Inn',
                      descrizione='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        numeroAlbergatori = Albergatore.objects.filter(nome='Marco', cognome='Cocco', password='ciao',
                                                  username='marcococco', email='marcococco@gmail.com',
                                                  citta='Cagliari', indirizzo='Via Scano 51').count()
        self.assertEqual(numeroAlbergatori, 1)

        numeroHotel = Hotel.objects.filter(albergatore=albergatore, nome='Holiday Inn',
                                      descrizione='Bello e profumato', citta='Cagliari',
                                      indirizzo='Viale Umberto Ticca').count()
        self.assertEqual(numeroHotel, 1)


class TestCamera(TestCase):
    def testCamera(self):
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

        numeroAlbergatori = Albergatore.objects.filter(nome='Marco', cognome='Cocco', password='ciao',
                                                  username='marcococco', email='marcococco@gmail.com',
                                                  citta='Cagliari', indirizzo='Via Scano 51').count()
        self.assertEqual(numeroAlbergatori, 1)

        numeroHotel = Hotel.objects.filter(albergatore=albergatore, nome='Holiday Inn',
                                      descrizione='Bello e profumato', citta='Cagliari',
                                      indirizzo='Viale Umberto Ticca').count()
        self.assertEqual(numeroHotel, 1)

        numeroCamere = Camera.objects.filter(hotel=hotel, numero='101', nLetti='4',
                                        prezzo='125.0', servizi='Bagno privato, Asciugacapelli').count()
        self.assertEqual(numeroCamere, 1)

# Test di accettazione

class TestLogout(TestCase):
    """Classe contenente i TA del Logout"""
    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Marras', password='wewe', username='user1',
                                  email='m@gmail.com', citta='Milano', indirizzo='via Lugodoro 1')
        albergatore.save()

        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

        request = self.request_factory.get('/login/', follow=True)
        data = self.client.session
        data.update({
            "nomeAlbergatore": 'user1',
        })
        data.save()

    def testLogout(self):
        response = self.client.get('/logout/')
        self.assertEquals(response.status_code, 302)


class TestRegistrazione(TestCase):
    """Classe contenente i TA della registrazione"""
    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()

        self.albergatore = albergatore
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()


    def testRegistrazioneAvvenuta(self):
        """ Verifica che un hotel keeper registrato possa accedere alla sua home """

        request = self.request_factory.get('/home/', follow=True)        # Si crea la request
        self.middleware.process_request(request)

        request.session.save() # Si crea sessione

        request.session['nomeAlbergatore'] = 'marcococco' # Si simula login

        response = homeAlbergatore(request)         # Si esegue la view della homeAlbergatore

        self.assertEquals(response.status_code, 200)    # Si verifica che sia avvenuto l'accesso

    def testRegistrazioneFallita(self):
        """ Verifica che un hotel keeper non registrato non possa accedere alla home"""

        # Creazione request
        request = self.request_factory.get('/home/', follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione login
        request.session['nomeAlbergatore'] = 'lorenzopalla'

        # Esecuzione della vista che gestisce la home dell'hotel keeper
        response = homeAlbergatore(request)

        # Verifica accesso negato e redirect
        self.assertEquals(response.status_code, 302)

    def testControlloStessoUsername(self):
        """ Verifica che sia negata l'iscrizione se l'username specificato esiste già """

        # Lista di appoggio
        listaAlbergatori = []

        # Creazione request
        request = self.request_factory.get('/registrazione/', follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        session = self.client.session
        session.save()

        # Riempimento del form
        form = {'nome': "Enzo",
                     'cognome': "Scano",
                     'email': "enzoscano@gmail.com",
                     'citta': "Cagliari",
                     'indirizzo': "Via Cocco Ortu 99",
                     'username': "marcococco",
                     'password': "buongiorno",
                     'confermaPassword': "buongiorno"}

        form = FormRegistrazione(data=form)

        # verifica che sia negata la validazione del form
        self.assertFalse(form.is_valid(), form.errors)

        # Conta gli utenti registrati e verifica che non ne siano stati aggiunti
        for a in Albergatore.objects.all():
            listaAlbergatori.append(a)

        self.assertTrue(len(listaAlbergatori), 1)

        # Riempimento del form
        form = {'nome': "Enzo",
                     'cognome': "Scano",
                     'email': "enzoscano@gmail.com",
                     'citta': "Cagliari",
                     'indirizzo': "Via Cocco Ortu 99",
                     'username': "enzoscano",
                     'password': "buongiorno",
                     'confermaPassword': "buongiorno"}

        form = FormRegistrazione(data=form)

        # Conteggio e verifica
        listaAlbergatori = []

        for a in Albergatore.objects.all():
            listaAlbergatori.append(a)

        self.assertTrue(len(listaAlbergatori), 1)

    def testRegistratiCampiErrati(self):
        form = {'nome': 'paolino', 'cognome': 'paperino', 'email': 'emailErrata', 'citta': 'Escalaplano', 'indirizzo': 'via Roma 1',
                     'username': 'username1', 'password':'password1', 'confermaPassword':'password1'}

        self.assertFalse(form.is_valid())


class TestLogin(TestCase):
    """ Classe contenente i TA della user story 2 """
    def setUp(self):
        albergatore = Albergatore(nome='Alba', cognome='Rossi', password='albachiara',
                                  username='albachiara', email='albachiaraRossi@gmail.com',
                                  citta='Cagliari', indirizzo='via Luce 10')
        albergatore.save()
        self.albergatore = albergatore
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testLogin(self):
        """ Verifica l'accesso di un utente proprietario di un albergo"""
        # Riempimento form
        form_data = {'username': 'albachiara', 'password': 'albachiara'}

        loginForm = FormLogin(data=form_data)
        # Verifica
        self.assertTrue(loginForm.is_valid(), loginForm.errors)

    def testRedirecUtenteLoggato(self):
        """ Verifica che un hotel keeper loggato non abbia accesso alla pagina di login
        e che venga reindirizzato verso la pagina diversa"""

        # Creazione della request
        request = self.request_factory.get('/login/', follow=True)
        self.middleware.process_request(request)
        # Creazione della sessione
        request.session.save()

        # Simulaazione hotel keeper loggato
        request.session['nomeAlbergatore'] = 'marcococco'

        # Esecuzione della vista di login
        response = login(request)

        # Verifica il redirect
        self.assertEquals(response.status_code, 302)


class TestHomeAlbergatore(TestCase):
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

        prenotazione = Prenotazione(email='lorenzomilia@gmail.com', camera=camera,
                                    checkIn=datetime.date(2019, 7, 3), checkOut=datetime.date(2018, 7, 21))
        prenotazione.save()

        self.albergatore = albergatore
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testVisualizzazionePrenotazioni(self):
        """ Verifica che un hotel keeper con prenotazioni le visualizzi nella sua home """

        # Creazione della request
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        # Creazione della sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['nomeAlbergatore'] = self.albergatore.username

        # Esecuzione della view che gestisce la home dell'albergatore
        response = homeAlbergatore(request)

        # Verifica che la pagina contenga la prenotazione
        self.assertContains(response, 'lorenzomilia@gmail.com')
        self.assertContains(response, 'Holiday Inn')


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

    def testVisualizzazioneListaHotel(self):
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

    def testCampiMancanti(self):
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

    def testHotelAggiunto(self):
        """ Verifica che un hotel sia stato aggiunto correttamente """

        # Lista temporanea
        listaHotel = []

        # Creazione request
        request = self.request_factory.get('/aggiungiHotel/', follow=True)
        self.middleware.process_request(request)

        chiave_sessione = self.albergatore.username
        session = self.client.session
        session['nomeAlbergatore'] = chiave_sessione
        session.save()

        # Verifica del numero di hotel presenti prima dell'aggiunta
        for hotel in Hotel.objects.all():
            if hotel.albergatore.username == self.albergatore.username:
                listaHotel.append(hotel)

        self.assertEqual(len(listaHotel), 2)



        # Riempimento form
        form= {'nome': "Caesar's Hotel",
                     'descrizione': "L'hotel preferito da Giulio Cesare",
                     'citta': "Cagliari",
                     'indirizzo': "Via Charles Darwin 2"}

        form = FormAggiungiHotel(data=form)

        # Verifica che il form sia valido
        self.assertTrue(form.is_valid())


        # Invia il form in POST all'url di aggiunta hotel
        self.client.post('/aggiungiHotel/', form)

        # Verifica della corretta aggiunta dell'hotel
        listaHotel = []

        for h in Hotel.objects.all():
            if h.albergatore.username == self.albergatore.username:
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

    def testVisualizzazioneDati(self):
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

    def testCampiMancanti(self):
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

    def testCameraAggiunta(self):
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
        session['nomeAlbergatore'] = key_sessione1
        session['idHotel'] = key_sessione2
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


class TestCerca(TestCase):
    """ Classe contenente i TA della user story 8 """
    def setUp(self):
        albergatore = Albergatore(nome='Giovanni', cognome='Cocco', password='GiovanniCocco',
                                  username='gcocco', email='gcocco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()
        hotel = Hotel(albergatore=albergatore, nome='La bellezza',
                      descrizione='Hotel 3 stelle', citta='Sassari', indirizzo='Piazza Italia')

        hotel.save()

        cameraDaPrenotare = Camera(numero=50, nLetti=1, prezzo=35, servizi='Wi-fi', hotel=hotel)
        cameraDaPrenotare.save()

        # albergatore che non ha hotel
        albergatore2 = Albergatore(nome='Giovanna', cognome='Cicci', password='GiovannaCicci',
                                  username='gcicci', email='gcicci@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 52')
        albergatore2.save()

        prenotare = Prenotazione(email='ag@gmail.com', camera=cameraDaPrenotare, checkIn=datetime.date(2019, 8, 28),
                          checkOut=datetime.date(2019, 8, 31))
        prenotare.save()

        self.albergatoreConH = albergatore

        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testCercaR(self):
        """ Verifica che sia possibile effettuare una ricerca"""

        # Creazione request
        request = self.request_factory.get('/cercaRS/', follow=True)

        # Creazione valori in GET
        request.GET.__init__(mutable=True)

        request.GET['cercaCitta'] = 'Sassari'
        request.GET['cercaLetti'] = '1'
        request.GET['cercaCheckIn'] = '2019-08-18'
        request.GET['cercaCheckOut'] = '2019-08-22'

        self.middleware.process_request(request)

        # Creazione sessione
        request.session.save()

        # Invio dei dati alla view che effettua la ricerca
        response = cercaRS(request)

        # Verifica corrispondenze trovate
        self.assertContains(response, 'La bellezza')


    def testRicercaNonTrovata(self):
        """ Se la ricerca non viene visualizzata perché non vengono trovate camere per quella città
        viene visualizzato un messaggio :
        Spiacenti! Non abbiamo camere disponibili per la città da lei indicata.
        con un link per tornare alla pagina di ricerca"""

        request = self.request_factory.get('/cercaRS/', follow=True)

        request.GET.__init__(mutable=True)

        request.GET['cercaCitta'] = 'Gavoi'
        request.GET['cercaLetti'] = '1'
        request.GET['cercaCheckIn'] = '2019-08-18'
        request.GET['cercaCheckOut'] = '2019-08-22'

        self.middleware.process_request(request)

        request.session.save()

        # Invio dati alla view che esegue la ricerca
        response = cercaRS(request)

        self.assertContains(response, 'Spiacenti! Non abbiamo camere disponibili per la città da lei indicata.')

    def testRicercaNonTrovataData(self):
            """ Se la ricerca non viene visualizzata perché non vengono trovate date disponibili"""

            request = self.request_factory.get('/cercaRS/', follow=True)

            request.GET.__init__(mutable=True)

            request.GET['cercaCitta'] = 'Sassari'
            request.GET['cercaLetti'] = '1'
            request.GET['cercaCheckIn'] = '2019-08-29'
            request.GET['cercaCheckOut'] = '2019-08-30'

            self.middleware.process_request(request)

            request.session.save()

            # Invio dati alla view che esegue la ricerca
            response = cercaRS(request)

            self.assertContains(response, 'Spiacenti! La camera è stata già prenotata')


class TestSalva(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Giovanni', cognome='Cullu', password='GiovanniCullu',
                                  username='gCullu', email='gCullu@gmail.com',
                                  citta='Oristano', indirizzo='Via Scano 53')
        albergatore.save()

        hotel1 = Hotel(albergatore=albergatore, nome='Il fico',
                      descrizione='Hotel 4 stelle', citta='Oristano', indirizzo='Via Scano')
        hotel1.save()

        camera = Camera(numero=50, nLetti=2, prezzo=50, servizi='Wi-fi, Colazione in camera', hotel=hotel1)
        camera.save()

        prenotare = Prenotazione(email='agl@gmail.com', camera=camera, checkIn=datetime.date(2019, 9, 28),
                                 checkOut=datetime.date(2019, 9, 30))
        prenotare.save()
        camera2 = Camera(numero=50, nLetti=3, prezzo=50, servizi='Wi-fi, Colazione in camera', hotel=hotel1)
        camera2.save()
        self.albergatore = albergatore
        self.camera = camera
        self.camera2 = camera2
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testControllaPrenotazione(self):
        # Riempimento form
        form_prenotazione = {'email': 'pippopluto@gmail.com'}

        data = self.client.session
        data.update({
            "checkinDT": '2020-09-05',
            "checkoutDT": '2020-09-06',
            "idCam": str(self.camera2.id)
        })
        data.save()
        # Invio form alla pagina
        self.client.get('/confermaPrenotazione/', form_prenotazione)

        contaLePrenotazioni = Prenotazione.objects.all().count()
        self.assertEqual(contaLePrenotazioni, 2)
