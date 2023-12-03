from django.db import models
from hotel_panel.models import FoodMenu
from accounts.models import MyUser


class Shopping(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.PROTECT)
    total_amount = models.FloatField()

# Create your models here.
