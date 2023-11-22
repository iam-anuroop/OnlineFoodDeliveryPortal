from django.contrib import admin
from .models import AvailableLocation


class  AvailableLocationAdmin(admin.ModelAdmin):
    list_display = ('country','state','district','city','location')
admin.site.register(AvailableLocation,AvailableLocationAdmin)


# Register your models here.
