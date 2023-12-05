from django.contrib.gis.db import models
from hotel_panel.models import FoodMenu
from accounts.models import MyUser
from delivery_boy.models import DeliveryPerson


class Shopping(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, db_index=True)
    item = models.ForeignKey(FoodMenu, on_delete=models.PROTECT, db_index=True)
    del_location = models.PointField(srid=4326, null=True, blank=True, db_index=True)
    address = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    total_amount = models.FloatField()

    is_canceled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.item} - {self.status}"


class DeliveryNotification(models.Model):
    STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    shopping = models.ForeignKey(Shopping, on_delete=models.PROTECT)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.PROTECT)


class ShoppingDeliveryPerson(models.Model):
    STATUS_CHOICES = [
        ("ordered", "Ordered"),
        ("purchasing", "Purchasing"),
        ("on_the_way", "On The Way"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
    ]
    shopping = models.ForeignKey(Shopping, on_delete=models.PROTECT)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


# Create your models here.
