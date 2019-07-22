import datetime
from django import forms
from .models import *
from django.contrib.auth.hashers import make_password, check_password


class FormRegistrazione(forms.Form):
    # Variabili da inserire
    nome = forms.CharField(label="Nome", required=True, max_length=100, )
    nome.widget.attrs.update({'class': 'margin form-control', "placeholder": "Nome"})
    cognome = forms.CharField(label="Cognome", required=True, max_length=100)
    cognome.widget.attrs.update({'class': 'margin form-control', "placeholder": "Cognome"})
    email = forms.EmailField(label="Email", required=True)
    email.widget.attrs.update({'class': 'margin form-control', "placeholder": "Email"})

    username = forms.CharField(label="Username", required=True)
    username.widget.attrs.update({'class': 'margin form-control', "placeholder": "Username"})
    password = forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)
    password.widget.attrs.update({'class': 'margin form-control', "placeholder": "Password"})
    confermaPassword = forms.CharField(widget=forms.PasswordInput(), label="Conferma Password", required=True)
    confermaPassword.widget.attrs.update({'class': 'margin form-control', "placeholder": "Conferma Password"})

    def clean_username(self):
        """ Override del metodo clean_data del campo username, si controlla che l'username sia disponibile"""
        username = self.cleaned_data["username"]

        if Albergatore.objects.filter(username=username).exists():
            raise forms.ValidationError('Username non disponibile!')
        else:
            return username

    def clean_confermaPassword(self):
        """"" Override del metodo clean_data del campo confermaPassword, si controlla che password e confermaPassword siano uguali"""

        if self.cleaned_data["confermaPassword"] != self.cleaned_data["password"]:
            raise forms.ValidationError('La password non è stata confermata correttamente')
        # La password viene criptata per essere salvata
        passwordCriptata = make_password(password=self.cleaned_data["password"])

        return passwordCriptata


class FormLogin(forms.Form):
    # Variabili da inserire
    username = forms.CharField(label="Username", required=True, max_length=100,
                               widget=forms.TextInput(attrs={"placeholder": "Nome", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))

    def clean_username(self):
        """ Override del metodo clean_data del campo username, si controlla che l'username sia presente nel DB"""
        username = self.cleaned_data["username"]
        if not Albergatore.objects.filter(username=username).exists():
            raise forms.ValidationError("Username non registrato")
        else:
            return username

    def clean_password(self):
        """ Override del metodo clean_data del campo username, si controlla che la password corrisponda"""
        passwordCorretta = False
        try:
            # Se l'username è registrato si salva l'albergatore con quell'username
            if Albergatore.objects.filter(username=self.cleaned_data["username"]).exists():
                albergatore = Albergatore.objects.get(username=self.cleaned_data["username"])

        except:

            raise forms.ValidationError("Utente non registrato")

        # Verifica la corrispondenza tra password inserita e quella salvata nel database
        if check_password(self.cleaned_data['password'], albergatore.password):
            passwordCorretta = True
        else:  # Assegno un valore True nel caso la password non criptata sia uguale a quella sul DB (non criptata)
            if str(self.cleaned_data["password"]) == albergatore.password:
                passwordCorretta = True

        if passwordCorretta:
            password = albergatore.password
        else:
            raise forms.ValidationError('Password errata!')

        return password


class FormAggiungiHotel(forms.Form):
    # Variabili da inserire
    nome = forms.CharField(required=True, max_length=100,
                           widget=forms.TextInput(attrs={"placeholder": "Nome", "class": "form-control"}))
    descrizione = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={"placeholder": "Descrizione", "class": "form-control"}))
    citta = forms.CharField(label="Città", required=True, max_length=100,
                            widget=forms.TextInput(attrs={"placeholder": "Città", "class": "form-control"}))
    indirizzo = forms.CharField(required=True, max_length=100,
                                widget=forms.TextInput(attrs={"placeholder": "Indirizzo", "class": "form-control"}))


class FormAggiungiCamera(forms.Form):
    # Variabili da inserire
    numero = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder": "Numero stanza","class": "form-control"}))
    nLetti = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder": "Numero letti","class": "form-control"}))
    prezzo = forms.FloatField(required=True, widget=forms.TextInput(attrs={"placeholder": "Prezzo","class": "form-control"}))
    servizi = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Servizi", "class": "form-control"}))
    

class FormRicerca(forms.Form):
    # Variabili da inserire
    SCELTA = (('0', 'Numero posti letto'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    cercaCitta = forms.CharField(label='', required=True, max_length=100,
                                 widget=forms.TextInput(attrs={"placeholder": "Città", "class": "form-control"}))
    cercaCitta.widget.attrs.update({'class': 'margin form-control'})
    cercaLetti = forms.ChoiceField(required=True, label="", widget=forms.Select, choices=SCELTA)
    cercaLetti.widget.attrs.update({'class': 'btn btn-default dropdown-toggle whiteBack margin'})
    cercaCheckIn = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today(), label="Da:")
    cercaCheckIn.widget.attrs.update({'class': 'margin form-control '})
    cercaCheckOut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today(), label="A:")
    cercaCheckOut.widget.attrs.update({'class': 'margin form-control  '})


class FormConferma(forms.Form):
    # Variabili da inserire
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control centrareBene margin', 'placeholder': 'Email'}))


