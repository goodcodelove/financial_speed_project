from django.contrib import admin
from .models import Profile, Commande, Carte

# Register your models here.

admin.site.register(Profile)
admin.site.register(Carte)
admin.site.register(Commande)