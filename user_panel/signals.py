from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShoppingPayment, DeliveryNotification, Shopping
from delivery_boy.models import DeliveryPerson

# from django.contrib.gis.db.models import Point, Distance
from django.contrib.gis.measure import D


@receiver(post_save, sender=ShoppingPayment)
def sendNotification(sender, instance, created, *args, **kwargs):
    if created:
        shopping = ShoppingPayment.objects.filter(id=instance.id).values().first()
        # del_loc = shopping['del_location']
        hotel_loc = shopping["hotel_loc"]
        delivery_peoples = DeliveryPerson.objects.filter(
            location__distance_lte=(hotel_loc, D(km=50)), is_approved=True
        )
        for delivery_person in delivery_peoples:
            DeliveryNotification.objects.create(
                shooping_payment=instance, delivery_person=delivery_person
            )
