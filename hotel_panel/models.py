# from django.db import models
from django.contrib.gis.db import models
from accounts.models import MyUser

class HotelOwner(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.PROTECT,related_name='hotelowner',null=True,blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    id_proof = models.CharField(null=True,blank=True)
    id_number = models.CharField(max_length=255,null=True,blank=True)



class HotelsAccount(models.Model):
    owner = models.ForeignKey(HotelOwner,on_delete=models.PROTECT,related_name='hotelaccount')
    hotel_name = models.CharField(max_length=255)
    description = models.TextField()
    contact = models.CharField(max_length=100)
    alt_contact = models.CharField(max_length=100)
    certificate = models.CharField()
    email = models.EmailField(unique=True)
    address = models.TextField()
    location = models.PointField(srid=4326)
    rating = models.FloatField()

    is_active = models.BooleanField(default=False)
    is_logined = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)



class FoodMenu(models.Model):
    hotel = models.ForeignKey(HotelsAccount,on_delete=models.CASCADE,related_name='foodmenu')
    food_name = models.CharField(max_length=255)
    food_type = models.CharField(max_length=255)
    food_image = models.CharField()
    food_price = models.FloatField()
    description = models.TextField()

    is_veg = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)




# Create your models here.
