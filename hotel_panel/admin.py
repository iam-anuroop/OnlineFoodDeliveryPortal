from django.contrib import admin
from .models import HotelOwner,HotelsAccount
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin

class MyOwnerAdmin(admin.ModelAdmin):
    list_display = ('id','contact','email')
admin.site.register(HotelOwner,MyOwnerAdmin)


class HotelAccountAdmin(OSMGeoAdmin):
    list_display = ('id','contact','email')
admin.site.register(HotelsAccount,HotelAccountAdmin)

# Register your models here.
