from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HotelOwner,HotelsAccount


@receiver(post_save,sender = HotelOwner)
def CreateHotel(sender,instance,created,*args, **kwargs):
    if created:
        HotelsAccount.objects.create(
            owner=instance
        )
