from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
# UserModel = get_user_model()
from .forms import CustomUserCreationForm, CommandeForm
from .tokens import account_activation_token
from .models import Commande, Carte, Contact

# Create your views here.

def index(request):

	return render(request, 'index.html')

def activation_sent_view(request):
    return render(request, 'activation_sent.html')


@transaction.atomic
def signup(request):
	
	if request.method == 'POST':

		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			mail_subject = 'Activate your account'
			current_site = get_current_site(request)
			message = render_to_string('acc_activate_email.html', {
				'user' : user,
				'domain' : current_site.domain,
				'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
				'token' : default_token_generator.make_token(user),
			})
			to_email = form.cleaned_data['email']
			email = EmailMessage(
				mail_subject, message, to=[to_email]
				)
			email.send()
			return redirect('transactions:activation_sent')

	else:
		form = CustomUserCreationForm()

	return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
	try:

		uid = urlsafe_base64_decode(uidb64).decode()
		user = User.objects.get(pk=uid)

	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and default_token_generator.check_token(user, token):

		user.is_active = True
		user.save()
		login(request, user)
		return redirect('index')

	else:

		return render(request, 'activation_invalid.html')



def cartes(request):
    cartes = Carte.objects.filter(disponible=True)
    context = {
        'cartes':cartes
    }
    return render(request, 'cartes.html', context)

@login_required(login_url = 'login')
@transaction.atomic
def carte(request, carte_id):

    carte = get_object_or_404(Carte, pk=carte_id)
    user = request.user
    context = {
        'user_id':user.id,
        'carte_id':carte.id,
        'libelle':carte.libelle,
        'prix' : carte.prix,
        'picture': carte.picture.url,
        'description': carte.description,
    }

    if request.method == 'POST':

        form = CommandeForm(request.POST)
        if form.is_valid():
            agence=form.cleaned_data['agence']
            relais=form.cleaned_data['relais']
            nom=form.cleaned_data['nom']
            prenom=form.cleaned_data['prenom']
            telephone=form.cleaned_data['telephone']
            try:
                with transaction.atomic():
                    carte=get_object_or_404(Carte, pk=carte_id)
                    c=Commande.objects.create(
                    agence=agence,
                    relais = relais,
                    nom=nom,
                    prenom=prenom,
                    carte=carte,
                    telephone=telephone,
                    user=user
                    )
                    email = EmailMessage(
                        subject = 'Commande',
                        from_email = 'noreply@financial-speed.com',
                        body = """Une nouvelle commande a été enregistrée. Connectez-vous à  l'admin pour les details de la commande""",
                        to = ['noreply@financial-speed.com',],
                        headers={'Content-Type': 'text/plain'},
                    )
                    email.send()
                    email1 = EmailMessage(
                        subject = 'Achat chez financial-speed.com',
                        from_email = 'noreply@financial-speed.com',
                        body = "Votre opération a été validée. rendez-vous en agence pour retirer votre carte",
                        to = [user.email],
                        headers={'Content-Type': 'text/plain'},
                    )
                    email1.send()
                    return render(request, 'merci.html', {'agence' : agence})
            except  IntegrityError:
                form.errors['internal'] = "Une erreur est survenue.Merci de reprendre votre commande"       
    else:
        form = CommandeForm()
    context['errors'] = form.errors.items() 
    context['form'] = form
    return render(request, 'carte.html', context)


def promo(request):
    cartes = Carte.objects.filter(promo=True)
    context = {
        'cartes_promo' : cartes,
    }
    return render(request, 'promotion.html', context)

# @login_required(login_url = 'transactions:login')
def transfert(request):
    return render(request, 'transfert.html')


def achat_crypto(request):
    return render(request, 'crypto_achat.html')

def vendre_crypto(request):
    return render(request, 'vendre_crypto.html')