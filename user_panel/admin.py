from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import (
    Shopping,
    ShoppingDeliveryPerson,
    ShoppingPayment,
    DeliveryNotification
    )


class ShoppingAdmin(OSMGeoAdmin):
    list_display = ("id", "item", "payment_id",'total_amount')
admin.site.register(Shopping,ShoppingAdmin)
# Register your models here.
