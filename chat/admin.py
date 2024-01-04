# admin.py

from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "content", "timestamp")


admin.site.register(Message, MessageAdmin)


# Register your models here.
