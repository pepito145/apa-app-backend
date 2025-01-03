from django.db import models
from django.utils.timezone import now

# Modèle existant pour les utilisateurs
class UserLogin(models.Model):
    email = models.EmailField(unique=True)  # Champ pour l'email
    password = models.CharField(max_length=255)  # Champ pour le mot de passe
    first_name = models.CharField(max_length=150, blank=True, null=True)  # Champ pour le prénom
    last_name = models.CharField(max_length=150, blank=True, null=True)  # Champ pour le nom
    date_joined = models.DateTimeField(default=now)  # Champ pour la date d'inscription
    clientid = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    code = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    access_token = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    refresh_token = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL

    class Meta:
        db_table = 'users_login'  # Nouveau nom pour la table

    def __str__(self):
        return self.email

# Nouveau modèle pour stocker les informations supplémentaires
class UsersInfos(models.Model):
    user = models.OneToOneField(UserLogin, on_delete=models.CASCADE, related_name='infos')
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    ipaq_score = models.IntegerField(blank=True, null=True)  # Permet NULL


    class Meta:
        db_table = 'users_infos'