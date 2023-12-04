from django.contrib.gis.db import models
from accounts.models import MyUser




class DeliveryPerson(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.PROTECT,null=True,blank=True)
    full_name = models.CharField(max_length=255,null=True,blank=True)
    location = models.PointField(srid=4326,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    delivery_area = models.PointField(srid=4326,null=True,blank=True)
    profile_photo = models.TextField(null=True,blank=True)
    id_proof = models.TextField(null=True,blank=True)







# Create your models here.