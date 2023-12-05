from django.contrib import admin
from .models import AvailableLocation
from django.contrib.gis.admin import OSMGeoAdmin


class AvailableLocationAdmin(OSMGeoAdmin):
    list_display = ("country", "state", "district", "city", "location")


admin.site.register(AvailableLocation, AvailableLocationAdmin)


# Register your models here.
