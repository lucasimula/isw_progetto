from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from .models import *
from .views import *
import datetime

# Test di accettazione

class TestLogout(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Marras', password='wewe', username='user1',
                                  email='m@gmail.com')
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
        """ Verifica che un albergatore loggato possa effettuare il logout """

        response = self.client.get('/logout/')
        self.assertEquals(response.status_code, 302)  # Si controlla che il redirect sia avvenuto correttamente


class TestRegistrazione(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com')
        albergatore.save()

        self.albergatore = albergatore
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testRegistrazioneAvvenuta(self):
        """ Verifica che un albergatore registrato possa accedere alla sua pagina """

        request = self.request_factory.get('/home/', follow=True)  # Si crea la request
        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        request.session['nomeAlbergatore'] = 'marcococco'  # Si simula il login

        response = homeAlbergatore(request)  # Si esegue la view della homeAlbergatore

        self.assertEquals(response.status_code, 200)  # Si verifica che sia avvenuto l'accesso

    def testControlloStessoUsername(self):
        """ Verifica che un utente non possa registrarsi se l'username scelto appartiene a un altro utente"""

        listaAlbergatori = []  # Si usa una lista di appoggio per controllare i dati

        request = self.request_factory.get('/registrazione/', follow=True)  # Si crea la request
        self.middleware.process_request(request)

        session = self.client.session  # Si crea la sessione
        session.save()

        form_data = {'nome': "Enzo",  # Si riempie il form
                     'cognome': "Scano",
                     'email': "enzoscano@gmail.com",
                     'username': "marcococco",
                     'password': "buongiorno",
                     'confermaPassword': "buongiorno"}

        form = FormRegistrazione(data=form_data)

        self.assertFalse(form.is_valid(), form.errors)  # Si verifica che sia negata la validazione del form

        for a in Albergatore.objects.all():  # Si contano gli utenti registrati
            listaAlbergatori.append(a)

        self.assertTrue(len(listaAlbergatori), 1)  # Si verifica che non siano stati aggiunti utenti

        form_data = {'nome': "Enzo",  # Si riempie il form
                     'cognome': "Scano",
                     'email': "enzoscano@gmail.com",
                     'username': "enzoscano",
                     'password': "buongiorno",
                     'confermaPassword': "buongiorno"}

        form = FormRegistrazione(data=form_data)

        listaAlbergatori = []

        for a in Albergatore.objects.all():  # Si contano gli utenti registrati
            listaAlbergatori.append(a)

        self.assertTrue(len(listaAlbergatori), 1)  # Si verifica che non siano stati aggiunti utenti

    def testRegistratiCampiErrati(self):
        """ Verifica che un utente non possa registrarsi se i campi del form sono compilati in modo errato """

        form_data = {'nome': 'paolino', 'cognome': 'paperino', 'email': 'emailErrata',  # Si riempie il form
                     'username': 'username1', 'password': 'password1', 'confermaPassword': 'password1'}

        formReg = FormRegistrazione(data=form_data)
        self.assertFalse(formReg.is_valid())  # Si verifica che sia negata la validazione del form


class TestLogin(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Alba', cognome='Rossi', password='albachiara',
                                  username='albachiara', email='albachiaraRossi@gmail.com')
        albergatore.save()
        self.albergatore = albergatore
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testLogin(self):
        """ Verifica che un albergatore registrato possa effettuare l'accesso correttamente """

        form_data = {'username': 'albachiara', 'password': 'albachiara'}  # Si riempie il form
        loginForm = FormLogin(data=form_data)

        self.assertTrue(loginForm.is_valid(), loginForm.errors)  # Si verifica che il form sia validato

    def testUtenteNonRegistrato(self):
        """ Verifica che un utente non registrato non possa accedere alla home personale degli albergatori """

        request = self.request_factory.get('/home/', follow=True)  # Si crea la request
        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        request.session['nomeAlbergatore'] = 'lorenzopalla'  # Si simula il login

        response = homeAlbergatore(request)  # Si esegue la view homeAlbergatore

        self.assertEquals(response.status_code, 302)  # Si verifica che l'utente non registrato sia reindirizzato

    def testUtenteLoggato(self):
        """ Verifica che un albergatore già loggato non abbia accesso alla pagina di login """

        request = self.request_factory.get('/login/', follow=True)   # Si crea la request
        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        request.session['nomeAlbergatore'] = 'marcococco'  # Si simula il login

        response = login(request)  # Si esegue la view login

        self.assertEquals(response.status_code, 302)  # Si verifica che l'utente reigstrato sia reindirizzato


class TestHomeAlbergatore(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com')
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
        """ Verifica che un albergatore visualizzi le prenotazioni delle camere dei suoi hotel """

        request = self.request_factory.get('/home/')  # Si crea la request
        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        request.session['nomeAlbergatore'] = self.albergatore.username   # Si simula il login

        response = homeAlbergatore(request)  # Si esegue la view homeAlbergatore

        self.assertContains(response, 'lorenzomilia@gmail.com')  # Si verifica che la pagina contenga i dati della prenotazione
        self.assertContains(response, 'Holiday Inn')


class TestListaHotel(TestCase):

    def setUp(self):
        albergatore1 = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                   username='marcococco', email='marcococco@gmail.com')
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
                                   username='enzoscano', email='enzoscano@gmail.com')
        albergatore2.save()

        self.albergatoreConHotel = albergatore1
        self.albergatoreSenzaHotel = albergatore2
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testVisualizzazioneListaHotel(self):
        """ Verifica che un albergatore visualizzi correttamente la lista dei suoi hotel """

        request = self.request_factory.get('/listaHotel/')  # Si crea la request
        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        request.session['nomeAlbergatore'] = self.albergatoreConHotel.username  # Si simula il login

        response = listaHotel(request)  # Si esegue la view listaHotel

        self.assertContains(response, 'Holiday Inn')  # Si verifica che la pagina contenga i dati degli hotel
        self.assertContains(response, 'T Hotel')


class TestAggiungiHotel(TestCase):

    def setUp(self):
        albergatore1 = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                   username='marcococco', email='marcococco@gmail.com')
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
                                   username='enzoscano', email='enzoscano@gmail.com')
        albergatore2.save()

        self.albergatore = albergatore1
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testHotelCampiMancanti(self):
        """ Verifica che non sia accettato un form incompleto """

        request = self.request_factory.get('/aggiungiHotel/', follow=True)  # Si crea la request
        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        request.session['nomeAlbergatore'] = self.albergatore.username  # Si simula il login

        form_data = {'nome': "Caesar's Hotel",  # Si riempie il form
                     'descrizione': "L'hotel preferito da Giulio Cesare",
                     'citta': "Cagliari",
                     'indirizzo': "Via Charles Darwin 2"}

        form = FormAggiungiHotel(data=form_data)

        self.assertTrue(form.is_valid(), msg=form.errors)  # Si verifica la validazione del form

    def testHotelAggiunto(self):
        """ Verifica che un hotel sia stato aggiunto correttamente """

        listaHotel = []  # Si usa una lista di appoggio per controllare i dati

        request = self.request_factory.get('/aggiungiHotel/', follow=True)  # Si crea la request
        self.middleware.process_request(request)

        chiave_sessione = self.albergatore.username
        session = self.client.session
        session['nomeAlbergatore'] = chiave_sessione
        session.save()

        for hotel in Hotel.objects.all():
            if hotel.albergatore.username == self.albergatore.username:
                listaHotel.append(hotel)

        self.assertEqual(len(listaHotel), 2)  # Si verifica il numero di hotel presenti inizialmente

        form_data = {'nome': "Caesar's Hotel",  # Si riempie il form
                     'descrizione': "L'hotel preferito da Giulio Cesare",
                     'citta': "Cagliari",
                     'indirizzo': "Via Charles Darwin 2"}

        form = FormAggiungiHotel(data=form_data)

        self.assertTrue(form.is_valid())  # Si verifica la validazione del form

        self.client.post('/aggiungiHotel/', form_data)  # Si inviano i dati del form tramite POST

        listaHotel = []

        for h in Hotel.objects.all():
            if h.albergatore.username == self.albergatore.username:
                listaHotel.append(h)

        self.assertEqual(len(listaHotel), 3)  # Si verifica l'aggiunta del nuovo hotel


class TestGestioneHotel(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com')
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

    def testVisualizzazioneDatiHotel(self):
        """ Verifica che un albergatore possa visualizzare i dati dell'hotel e delle camere che contiene """

        request = self.request_factory.get('/gestioneHotel/?id=' + str(self.hotel.id), follow=True)  # Si crea la request
        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        request.session['nomeAlbergatore'] = self.albergatore.username  # Si simula il login

        response = gestioneHotel(request)

        self.assertContains(response, 'Holiday Inn')  # Si verifica che la risposta contenga i dati dell'hotel
        self.assertContains(response, '101')
        self.assertContains(response, '4')
        self.assertContains(response, '125.0')


class TestAggiungiCamera(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com')
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

    def testCameraCampiMancanti(self):
        """ Verifica che non sia accettato un form incompleto """

        request = self.request_factory.get('/aggiungiCamera/', follow=True)
        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        request.session['nomeAlbergatore'] = self.albergatore.username  # Si simula il login
        request.session['idHotel'] = self.hotel.id    # Si simula l'inserimento dell'id dell'hotel in sessione

        form_data = {'numero': "202",  # Si riempie il form
                     'nLetti': "2",
                     'prezzo': "62.0",
                     'servizi': "Colazione inclusa, Asciugacapelli"}

        form = FormAggiungiCamera(data=form_data)

        self.assertTrue(form.is_valid(), msg=form.errors)  # Verifica la validazione del form

    def testCameraAggiunta(self):
        """ Verifica che una camera venga aggiunta correttamente """

        listaCamere = []  # Si usa una lista di appoggio per controllare i dati

        request = self.request_factory.get('/aggiungiCamera/?id=' + str(self.hotel.id), follow=True)  # Si crea la request
        self.middleware.process_request(request)

        key_sessione1 = str(self.albergatore.username)  # Si crea la sessione e si inseriscono i parametri necessari
        key_sessione2 = str(self.hotel.id)
        session = self.client.session
        session['nomeAlbergatore'] = key_sessione1
        session['idHotel'] = key_sessione2
        session.save()

        form_data = {'numero': "202",  # Si riempie il form
                     'nLetti': "2",
                     'prezzo': "62.0",
                     'servizi': "Colazione inclusa, Asciugacapelli"}

        form = FormAggiungiCamera(data=form_data)

        self.assertTrue(form.is_valid())  # Si verifica la validazione del form

        for c in Camera.objects.all():
            if c.hotel == self.hotel:
                listaCamere.append(c)

        self.assertEqual(len(listaCamere), 1)  # Si verifica il numero delle camere prima dell'aggiunta

        form_data = {'numero': "303",  # Si riempie il form
                     'nLetti': "3",
                     'prezzo': "180.0",
                     'servizi': "Colazione inclusa, Bagno privato, TV, Asciugacapelli"}

        self.client.post('/aggiungiCamera/', form_data)  # Si inviano i dati del form tramite POST

        listaCamere = []

        for c in Camera.objects.all():
            if c.hotel == self.hotel:
                listaCamere.append(c)

        self.assertEqual(len(listaCamere), 2)  # Si verifica il numero delle camere dopo l'aggiunta


class TestCerca(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Giovanni', cognome='Cocco', password='GiovanniCocco',
                                  username='gcocco', email='gcocco@gmail.com')
        albergatore.save()
        hotel = Hotel(albergatore=albergatore, nome='La bellezza',
                      descrizione='Hotel 3 stelle', citta='Sassari', indirizzo='Piazza Italia')

        hotel.save()

        cameraDaPrenotare = Camera(numero=50, nLetti=1, prezzo=35, servizi='Wi-fi', hotel=hotel)
        cameraDaPrenotare.save()

        albergatore2 = Albergatore(nome='Giovanna', cognome='Cicci', password='GiovannaCicci',        # Albergatore che non ha hotel
                                   username='gcicci', email='gcicci@gmail.com')
        albergatore2.save()

        prenotare = Prenotazione(email='ag@gmail.com', camera=cameraDaPrenotare, checkIn=datetime.date(2019, 8, 28),
                                 checkOut=datetime.date(2019, 8, 31))
        prenotare.save()

        self.albergatoreConH = albergatore

        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testRicerca(self):
        """ Verifica che un utente possa effettuare una ricerca """

        request = self.request_factory.get('/cercaRS/', follow=True)  # Si crea la request

        request.GET.__init__(mutable=True)

        request.GET['cercaCitta'] = 'Sassari'  # Si inseriscono i valori all'interno della GET
        request.GET['cercaLetti'] = '1'
        request.GET['cercaCheckIn'] = '2019-08-18'
        request.GET['cercaCheckOut'] = '2019-08-22'

        self.middleware.process_request(request)

        request.session.save()  # Si crea la sessione

        response = cercaRS(request)  # Si esegue la view cercaRS

        self.assertContains(response, 'La bellezza')  # Si verifica che la risposta contenga i dati desiderati

    def testRicercaNonTrovata(self):
        """ Verifica che se la ricerca trova camere per la città scelta venga visualizzato un messaggio di errore """

        request = self.request_factory.get('/cercaRS/', follow=True)  # Si crea la request

        request.GET.__init__(mutable=True)

        request.GET['cercaCitta'] = 'Gavoi'  # Si inseriscono i valori all'interno della GET
        request.GET['cercaLetti'] = '1'
        request.GET['cercaCheckIn'] = '2019-08-18'
        request.GET['cercaCheckOut'] = '2019-08-22'

        self.middleware.process_request(request)

        request.session.save()

        response = cercaRS(request)  # Si esegue la view cercaRS

        self.assertContains(response, 'Spiacenti! Non abbiamo camere disponibili per la città da lei indicata.')  # Si verifica che la risposta contenga il messaggio d'errore

    def testRicercaNonTrovataData(self):
        """ Verifica che un utente non visualizzi risultati se le date scelte sono occupate """

        request = self.request_factory.get('/cercaRS/', follow=True)  # Si crea la request

        request.GET.__init__(mutable=True)

        request.GET['cercaCitta'] = 'Sassari'  # Si inseriscono i valori all'interno della GET
        request.GET['cercaLetti'] = '1'
        request.GET['cercaCheckIn'] = '2019-08-29'
        request.GET['cercaCheckOut'] = '2019-08-30'

        self.middleware.process_request(request)

        request.session.save()

        response = cercaRS(request)  # Si esegue la view cercaRS

        self.assertContains(response, 'Spiacenti! La camera è stata già prenotata')


class TestSalva(TestCase):

    def setUp(self):
        albergatore = Albergatore(nome='Giovanni', cognome='Cullu', password='GiovanniCullu',
                                  username='gCullu', email='gCullu@gmail.com')
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
        """ Verifica che una prenotazione corretta sia salvata correttamente """

        form_prenotazione = {'email': 'pippopluto@gmail.com'}  # Si riempie il form

        data = self.client.session
        data.update({
            "checkinDT": '2020-09-05',
            "checkoutDT": '2020-09-06',
            "idCam": str(self.camera2.id)
        })
        data.save()

        self.client.get('/confermaPrenotazione/', form_prenotazione)  # Si inviano i dati del form alla pagina

        contaLePrenotazioni = Prenotazione.objects.all().count()
        self.assertEqual(contaLePrenotazioni, 2)  # Si verifica che la prenotazione sia stata salvata
