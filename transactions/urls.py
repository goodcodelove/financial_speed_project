from django.urls import path, include
from . import views

app_name = 'transactions'

urlpatterns = [
	path('signup/', views.signup, name='signup'),
	path('cartes/', views.cartes, name='cartes'),
	path('carte/<int:carte_id>/', views.carte, name='carte'),
	path('promo/', views.promo, name="promo"),
	path('transfert/', views.transfert, name='transfert'),
	path('buycrypto/', views.achat_crypto, name='buy'),
	path('sellcrypto/', views.vendre_crypto, name='sell'),
	path('sent/', views.activation_sent_view, name='activation_sent'),
	path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]