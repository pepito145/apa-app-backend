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

# Physiological data model
class Physio(models.Model):
    email = models.OneToOneField(InfoUser, on_delete=models.CASCADE, primary_key=True, related_name='physio')
    date = models.DateTimeField(default=now)  # Record date
    steps = models.IntegerField(blank=True, null=True)  # Steps
    calories = models.IntegerField(blank=True, null=True)  # Calories burned
    bpm_avrg = models.IntegerField(blank=True, null=True)  # Average BPM

    class Meta:
        db_table = 'physio'

# BPM data model
class BPM(models.Model):
    email = models.ForeignKey(Physio, on_delete=models.CASCADE, related_name='bpm')
    bpm = models.IntegerField(blank=True, null=True)  # BPM value
    time = models.TimeField()  # Timestamp of the BPM reading

    class Meta:
        db_table = 'bpm'

# Session history model
class SessionsHist(models.Model):
    email = models.ForeignKey(InfoUser, on_delete=models.CASCADE, related_name='sessions_hist')
    start_date = models.DateTimeField()  # Session start time
    duration = models.IntegerField()  # Session duration
    calories = models.IntegerField(blank=True, null=True)  # Calories burned in the session
    nb_ex_comp = models.IntegerField()  # Number of exercises completed
    pain = models.IntegerField()  # Pain level reported
    user_difficulty = models.IntegerField()  # User's perceived difficulty
    ex_id = models.CharField(max_length=255)  # Exercise ID

    class Meta:
        db_table = 'sessions_hist'
        unique_together = ('email', 'start_date')  # Composite primary key

# Sessions model
class Sessions(models.Model):
    ses_id = models.AutoField(primary_key=True)  # Unique session ID
    ex_id = models.OneToOneField(SessionsHist, on_delete=models.CASCADE, unique=True, related_name='session')
    ses_difficulty = models.IntegerField()  # Session difficulty

    class Meta:
        db_table = 'sessions'

# Exercise sheets model
class ExerciseSheets(models.Model):
    id = models.AutoField(primary_key=True)  # Unique ID for the exercise
    image_src = models.URLField()  # URL for the exercise image
    consigne = models.TextField()  # Instructions for the exercise

    class Meta:
        db_table = 'exercise_sheets'

# Encouragements model
class Encouragements(models.Model):
    id = models.AutoField(primary_key=True)  # Unique ID for the message
    message = models.TextField()  # Encouragement message

    class Meta:
        db_table = 'encouragements'