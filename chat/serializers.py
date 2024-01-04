# serializers.py

from rest_framework import serializers
from .models import Message
from accounts.serializers import MyuserEmailSerializer


class MessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["content"]


class MessageGetSerializer(serializers.ModelSerializer):
    sender = MyuserEmailSerializer()

    class Meta:
        model = Message
        fields = ["content", "timestamp", "sender"]
