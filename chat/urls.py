# urls.py

from django.urls import path
from .views import SendMessageView, InboxView

urlpatterns = [
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    # Add more URLs as needed
]
