# models.py

from django.db import models
from accounts.models import MyUser
from user_panel.models import Shopping,ShoppingPayment


class Message(models.Model):
    order_id = models.ForeignKey(
        ShoppingPayment, on_delete=models.CASCADE, null=True, blank=True
    )
    sender = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,null=True, blank=True, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content}"


# Create your models here.
