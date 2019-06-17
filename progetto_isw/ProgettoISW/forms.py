from django import forms


class FormRegistrazione(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.PasswordInput()


class FormLogin(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.PasswordInput()


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