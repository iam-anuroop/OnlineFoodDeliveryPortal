from django.urls import path
from .views import SendMessageView

urlpatterns = [
    path("send-message/", SendMessageView.as_view(), name="send-message"),
]
