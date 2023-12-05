from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyUser, UserProfile


@receiver(post_save, sender=MyUser)
def CreateProfile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
