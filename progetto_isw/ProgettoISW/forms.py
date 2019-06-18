from django import forms
from .models import *
from django.contrib.auth.hashers import make_password


class FormRegistrazione(forms.Form):
    # Variabili da inserire
    nome = forms.CharField(label="Nome", required=True, max_length=100)
    cognome = forms.CharField(label="Cognome", required=True, max_length=100)
    email = forms.EmailField(label="Email", required=True)
    citta = forms.CharField(label="Citta")
    indirizzo = forms.CharField(label="Indirizzo")
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput())
    confermaPassword = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        # Override del metodo clean_data del campo username si controlla che l'username sia disponibile
        username = self.cleaned_data["username"]

        if Albergatore.objects.filter(username=username).exists():
            raise forms.ValidationError('Username non disponibile!')
        else:
            return username

    def clean_confermaPassword(self):
        # Override del metodo clean_data del campo confermaPassword, si controlla che password e confermaPassword siano uguali

        if self.cleaned_data["confermaPassword"] != self.cleaned_data["password"]:
             raise forms.ValidationError('La password non è stata confermata correttamente')
        # La password viene criptata per essere salvata
        passwordCriptata = make_password(password=self.cleaned_data["password"])

        return passwordCriptata


class FormLogin(forms.Form):
    nome = forms.CharField(label="Nome", required=True, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        # Viene controllato che l'username sia presente nel DB
        username = self.cleaned_data["username"]
        if not Albergatore.objects.filter(username=username).exists():
            raise forms.ValidationError("Username non registrato")
        else:
            return username

    def clean_password(self):
        # Si controlla la correttezza della password
        try:
            # Se l'username è registrato si salva l'albergatore con quell'username
            if Albergatore.objects.filter(username=self.cleaned_data["username"]).exists() :
                albergatore = Albergatore.objects.get(username=self.cleaned_data["username"])

        except:
            raise forms.ValidationError("Utente non registrato")

        # Verifica la corrispondenza tra password inserita e quella salvata nel database
        if albergatore.check_password(self.cleaned_data['password']):
            password = self.cleaned_data['password']
        else:
            raise forms.ValidationError('Password errata!')

        return password


class FormAggiungiHotel(forms.Form):
    nome = forms.CharField(label="Nome", required=True, max_length=100)
    descrizione = forms.CharField()
    citta = forms.CharField(max_length=100)
    indirizzo = forms.CharField(max_length=100)


class FormAggiungiCamera(forms.Form):
    numero = forms.IntegerField(required=True)
    nLetti = forms.IntegerField(required=True)
    prezzo = forms.FloatField(required=True)
    servizi = forms.CharField()
    

class FormPrenotazione(forms.Form):
    email = forms.EmailField(required=True)
    camera = forms.IntegerField(required=True)
    checkIn = forms.DateField(required=True)
    checkOut = forms.DateField(required=True)