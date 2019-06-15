from django import forms


class FormRegistrazione(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.PasswordInput()


class FormAggiungiHotel(forms.Form):
    nome = forms.CharField(label="Nome", required=True, max_length=100)
    descrizione = forms.TextField()
    indirizzo = forms.CharField(max_length=100)