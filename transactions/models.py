from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	localite = models.CharField(max_length=200, blank=False)
	sponsor = models.CharField(max_length=100, blank=False)
	avis = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return self.user.last_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

class Carte(models.Model):
	libelle = models.CharField(max_length=100)
	prix = models.IntegerField()
	description = models.CharField(max_length=1000)
	disponible = models.BooleanField(default=True)
	promo = models.BooleanField(default=False)
	picture = models.ImageField('image',upload_to='images/', blank=True)

	class Meta:
		verbose_name = 'Carte'

	def __str__(self):
		return self.libelle

class Commande(models.Model):
	
	CHOICES = [
    ('MARCORY', (
            ('MARCORY SANS FIL +225 58 73 77 63', 'MARCORY SANS FIL +225 58 73 77 63'),
            # ('ES', 'Spain'),
        )
    ),
    ('KOUMASSI', (
            ('MARCORY ETS TONY REMBLAIS COLLEGE COLOMBE +225 07215421', 'MARCORY ETS TONY REMBLAIS COLLEGE COLOMBE +225 07215421'),
            # ('DZ', 'Algeria'),
        )
    ),
    ]
	
	nom = models.CharField(max_length=30)
	prenom = models.CharField(max_length=100)
	telephone = models.CharField(max_length=12)
	relais = models.CharField(max_length=200, blank=True)
	agence = models.CharField(max_length = 100, choices=CHOICES, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	carte = models.ForeignKey(Carte, on_delete=models.CASCADE)
	date_commande = models.DateTimeField(auto_now_add=True)
	retiree = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Commande'

	def __str__(self):
		return self.nom


class Contact(models.Model):

	nom = models.CharField('nom', max_length=100)
	email = models.EmailField()
	sujet = models.CharField('sujet', max_length=150)
	message = models.CharField('message', max_length=2000)

	class Meta:
		verbose_name = 'Contact'

	def __str__(self):
		return self.nom