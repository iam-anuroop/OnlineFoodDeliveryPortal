from django.contrib import admin
from .models import HotelOwner, HotelsAccount, FoodMenu
from django.contrib.gis.admin import OSMGeoAdmin


from django.contrib.gis.admin import OSMGeoAdmin


class MyOwnerAdmin(admin.ModelAdmin):
    list_display = ("id", "contact", "email")


admin.site.register(HotelOwner, MyOwnerAdmin)


class HotelAccountAdmin(OSMGeoAdmin):
    list_display = ("id", "hotel_name", "contact", "email")


admin.site.register(HotelsAccount, HotelAccountAdmin)


class FoodMenuAdmin(admin.ModelAdmin):
    list_display = ("id", "food_name", "food_price")


admin.site.register(FoodMenu, FoodMenuAdmin)

# Register your models here.
