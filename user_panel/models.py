from django.contrib.gis.db import models
from hotel_panel.models import FoodMenu
from accounts.models import MyUser
from delivery_boy.models import DeliveryPerson



# class Shopping(models.Model):

#     STATUS_CHOICES = [
#         ('ordered', 'Ordered'),
#         ('on_delivery', 'On Delivery'),
#         ('delivered', 'Delivered'),
#     ]

#     user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
#     item = models.ForeignKey(FoodMenu, on_delete=models.PROTECT)
#     delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.PROTECT)
#     location = models.PointField(srid=4326,null=True,blank=True)
#     address = models.TextField(null=True,blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     date = models.DateTimeField(auto_now_add=True)
#     quantity = models.IntegerField()
#     total_amount = models.FloatField()

#     def __str__(self):
#         return f"{self.user} - {self.item} - {self.status}"



# Create your models here.
