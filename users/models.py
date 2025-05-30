from django.db import models
from django.utils.timezone import now

# Modèle existant pour les utilisateurs
class UserLogin(models.Model):
    email = models.EmailField(unique=True)  # Champ pour l'email
    password = models.CharField(max_length=255)  # Champ pour le mot de passe

    date_joined = models.DateTimeField(default=now)  # Champ pour la date d'inscription
    client_id = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    client_secret = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    
    user_id = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    code = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    access_token = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    refresh_token = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'users_login'  # Nouveau nom pour la table

    def __str__(self):
        return self.email

# Nouveau modèle pour stocker les informations supplémentaires
class UsersInfos(models.Model):
    login = models.OneToOneField(UserLogin, on_delete=models.CASCADE, related_name='infos')
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    ipaq_score = models.IntegerField(blank=True, null=True)  # Permet NULL
    streak = models.IntegerField(blank=True, null=True)  # Permet NULL
    XP = models.IntegerField(blank=True, null=True)  # Permet NULL
    level = models.IntegerField(blank=True, null=True)  # Permet NULL



    class Meta:
        db_table = 'users_infos'
        
class Activity(models.Model):
    user_id = models.CharField(max_length=150, blank=True, null=True)  # Permet NULL
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    date = models.DateTimeField(null=True)
    activity = models.CharField(max_length=20, blank=True, null=True)
    seance_id = models.IntegerField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)
    intensity = models.IntegerField(blank=True, null=True)
    hr_average = models.IntegerField(blank=True, null=True)
    hr_min = models.IntegerField(blank=True, null=True)
    hr_max = models.IntegerField(blank=True, null=True)
    
    
    class Meta:
        db_table = 'activity'
    
class Physio(models.Model):
    email = models.OneToOneField(UsersInfos, on_delete=models.CASCADE, primary_key=True, related_name='physio')
    date = models.DateTimeField(blank=True, null=True)  # Record date
    steps = models.IntegerField(blank=True, null=True)  # Steps
    calories = models.IntegerField(blank=True, null=True)  # Calories burned
    bpm_avrg = models.IntegerField(blank=True, null=True)  # Average BPM

    class Meta:
        db_table = 'physio'



# Sessions model
class Seances(models.Model):
    email = models.EmailField(blank=True, null=True)  # Champ pour l'email
    painLevel = models.IntegerField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    totalExercises = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True,null=True)
    activity_id = models.IntegerField(blank=True, null=True)
    
    frontend_id = models.CharField(max_length=20, blank=True, null=True)
    
    private_id = models.IntegerField(blank=True, null=True, unique = True)
    
    duration = models.IntegerField(blank=True, null=True)
    
    has_been_synced = models.BooleanField(default=False, null=True)
    
    start_time = models.DateTimeField(blank=True,null=True)
    
    
    def save(self, *args, **kwargs):
        if self.private_id is None:
            last_id = Seances.objects.aggregate(models.Max('private_id'))['private_id__max'] or 0
            self.private_id = last_id + 1
        super().save(*args, **kwargs)
        
    
    
    class Meta:
        db_table = 'Seances'

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


# BPM data model
class BPM(models.Model):
    email = models.ForeignKey(Physio, on_delete=models.CASCADE, related_name='bpm')
    bpm = models.IntegerField(blank=True, null=True)  # BPM value
    time = models.TimeField()  # Timestamp of the BPM reading

    class Meta:
        db_table = 'bpm'