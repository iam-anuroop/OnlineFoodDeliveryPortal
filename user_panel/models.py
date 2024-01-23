from django.contrib.gis.db import models
from hotel_panel.models import FoodMenu
from accounts.models import MyUser
from delivery_boy.models import DeliveryPerson


class ShoppingPayment(models.Model):
    STATUS_CHOICES = [
        ("success", "Success"),
        ("incomplete", "Incomplete"),
    ]
    stripe_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    total_amount = models.FloatField(null=True, blank=True)
    del_location = models.PointField(srid=4326, null=True, blank=True, db_index=True)
    address = models.TextField(null=True, blank=True)
    hotel_loc = models.PointField(srid=4326, null=True, blank=True, db_index=True)

    is_canceled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)


class Shopping(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, db_index=True)
    item = models.ForeignKey(FoodMenu, on_delete=models.PROTECT, db_index=True)
    payment_id = models.ForeignKey(
        ShoppingPayment, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()


class DeliveryNotification(models.Model):
    STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, null=True, blank=True
    )
    shooping_payment = models.ForeignKey(
        ShoppingPayment, on_delete=models.PROTECT, null=True, blank=True
    )
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.shooping_payment}"


class ShoppingDeliveryPerson(models.Model):
    STATUS_CHOICES = [
        ("ordered", "Ordered"),
        ("purchasing", "Purchasing"),
        ("on_the_way", "On The Way"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
    ]
    shopping_payment = models.ForeignKey(
        ShoppingPayment, on_delete=models.PROTECT, null=True, blank=True
    )
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


# Create your models here.
