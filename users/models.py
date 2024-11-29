from django.db import models
from django.utils.timezone import now

# Create your models here.
class UserLogin(models.Model):
    email = models.EmailField(unique=True)  # Champ pour l'email
    password = models.CharField(max_length=255)  # Champ pour le mot de passe
    first_name = models.CharField(max_length=150, blank=True, null=True)  # Champ pour le prénom
    last_name = models.CharField(max_length=150, blank=True, null=True)  # Champ pour le nom
    date_joined = models.DateTimeField(default=now)  # Champ pour la date d'inscription

    def __str__(self):
        return self.email