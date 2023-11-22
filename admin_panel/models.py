# from django.db import models
from django.contrib.gis.db import models




class AvailableLocation(models.Model):
    country = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    district = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    location = models.PointField(srid=4326,null=True,blank=True)



# Create your models here.
