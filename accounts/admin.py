from django.contrib import admin
from .models import MyUser,UserProfile
# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id','phone','email')
admin.site.register(MyUser,MyUserAdmin)


class UserProfileAdmin(OSMGeoAdmin):
    list_display = ('id','user_address','alt_phone','location')
admin.site.register(UserProfile,UserProfileAdmin)
