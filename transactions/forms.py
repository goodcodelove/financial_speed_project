from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm, EmailInput, TextInput, PasswordInput
from .models import Commande, Contact

class CustomUserCreationForm(UserCreationForm):

	class Meta:

		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
		widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }


class CommandeForm(ModelForm):
	class Meta:
		model = Commande
		fields = ('nom','prenom','telephone','relais','agence')


# class ContactForm(ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['nom', 'email', 'sujet', 'message']
#         widgets = {
#             'nom': TextInput(attrs={'class': 'form-control', 'id':'name', 'placeholder': 'Votre nom', 'data-rule':'minlen:4', 'data-msg':'Entrez un nom de 4 caractères minimum'}),
#             'email': EmailInput(attrs={'class': 'form-control', 'id':'email', 'placeholder':'Votre Email', 'data-rule':'email', 'data-msg':'Entrez un email valide '}),
#             'sujet': TextInput(attrs={'class': 'form-control', 'id':'subject', 'placeholder':'Sujet', 'data-rule':'minlen:4', 'data-msg':'Please enter at least 8 chars of subject'}),
#             'message': Textarea(attrs={'class': 'form-control', 'rows':'5', 'data-rule':'required', 'data-msg':'Please write something for us', 'placeholder':'Message'})
#         }

