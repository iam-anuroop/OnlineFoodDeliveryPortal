from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import (
    Shopping,
    ShoppingDeliveryPerson,
    ShoppingPayment,
    DeliveryNotification,
)


class ShoppingAdmin(OSMGeoAdmin):
    list_display = ("id", "item", "payment_id")


admin.site.register(Shopping, ShoppingAdmin)


class ShoppingPaymentAdmin(OSMGeoAdmin):
    list_display = ("id", "stripe_id")


admin.site.register(ShoppingPayment, ShoppingPaymentAdmin)


class DeliveryNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "delivery_person", "status")


admin.site.register(DeliveryNotification, DeliveryNotificationAdmin)


class ShoppingDeliveryPersonAdmin(admin.ModelAdmin):
    list_display = ("id", "delivery_person", "status")


admin.site.register(ShoppingDeliveryPerson, ShoppingDeliveryPersonAdmin)


# Register your models here.
