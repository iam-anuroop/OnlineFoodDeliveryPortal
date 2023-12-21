from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import (
    Shopping,
    ShoppingDeliveryPerson,
    ShoppingPayment,
    DeliveryNotification
    )


class ShoppingAdmin(OSMGeoAdmin):
    list_display = ("id", "item", "payment_id")
admin.site.register(Shopping,ShoppingAdmin)


class ShoppingPaymentAdmin(admin.ModelAdmin):
    list_display = ('id','stripe_id')
admin.site.register(ShoppingPayment,ShoppingPaymentAdmin)
# Register your models here.
