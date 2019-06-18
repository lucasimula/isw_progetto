from django.db import models

# Create your models here.


class Albergatore(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    citta = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=200)


class Hotel(models.Model):
    albergatore = models.ForeignKey(Albergatore, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    citta = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=100)


class Camera(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    numero = models.IntegerField()
    nLetti = models.IntegerField()
    prezzo = models.FloatField()
    servizi = models.TextField()


class Prenotazione(models.Model):
    email = models.EmailField()
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    checkIn = models.DateField()
    checkOut = models.DateField()