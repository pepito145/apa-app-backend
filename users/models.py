from django.db import models

# Create your models here.
class UserLogin(models.Model):
    email = models.EmailField(unique=True)  # Champ pour l'email
    password = models.CharField(max_length=255)  # Champ pour le mot de passe

    def __str__(self):
        return self.email