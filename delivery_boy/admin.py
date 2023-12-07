from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import DeliveryPerson


class DeliveryPersonAdmin(OSMGeoAdmin):
    list_display=['id']

admin.site.register(DeliveryPerson,DeliveryPersonAdmin)

# Register your models here.
