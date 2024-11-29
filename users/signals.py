from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserLogin, UsersInfos

@receiver(post_save, sender=UserLogin)
def create_user_infos(sender, instance, created, **kwargs):
    if created:
        UsersInfos.objects.create(user=instance)