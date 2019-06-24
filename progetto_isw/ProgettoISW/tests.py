from django.test import TestCase
from .models import *

# Create your tests here.

class TestHotel(TestCase):
    def test_Hotel(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()

        hotel = Hotel(albergatore=albergatore, nome='Holiday Inn',
                      description='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        nAlbergatori = Albergatore.objects.filter(nome='Marco', cognome='Cocco', password='ciao',
                                                  username='marcococco', email='marcococco@gmail.com',
                                                  citta='Cagliari', indirizzo='Via Scano 51').count()
        self.assertEqual(nAlbergatori, 1)

        nHotel = Hotel.objects.filter(albergatore=albergatore, nome='Holiday Inn',
                                      description='Bello e profumato', citta='Cagliari',
                                      indirizzo='Viale Umberto Ticca').count()
        self.assertEqual(nHotel, 1)


class TestCamera(TestCase):
    def test_camera(self):
        albergatore = Albergatore(nome='Marco', cognome='Cocco', password='ciao',
                                  username='marcococco', email='marcococco@gmail.com',
                                  citta='Cagliari', indirizzo='Via Scano 51')
        albergatore.save()

        hotel = Hotel(albergatore=albergatore, nome='Holiday Inn',
                      description='Bello e profumato', citta='Cagliari',
                      indirizzo='Viale Umberto Ticca')
        hotel.save()

        camera = Camera(hotel=hotel, numero='101', nLetti='4',
                        prezzo='125.00', servizi='Bagno privato, Asciugacapelli')
        camera.save()

        nAlbergatori = Albergatore.objects.filter(nome='Marco', cognome='Cocco', password='ciao',
                                                  username='marcococco', email='marcococco@gmail.com',
                                                  citta='Cagliari', indirizzo='Via Scano 51').count()
        self.assertEqual(nAlbergatori, 1)

        nHotel = Hotel.objects.filter(albergatore=albergatore, nome='Holiday Inn',
                                      description='Bello e profumato', citta='Cagliari',
                                      indirizzo='Viale Umberto Ticca').count()
        self.assertEqual(nHotel, 1)

        nCamere = Camera.objects.filter(hotel=hotel, numero='101', nLetti='4',
                                        prezzo='125.00', servizi='Bagno privato, Asciugacapelli')
        self.assertEqual(nCamere, 1)


# Test di accettazione

# da definire