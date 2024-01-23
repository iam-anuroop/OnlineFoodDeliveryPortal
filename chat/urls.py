from django.urls import path
from .views import (
    SendMessageView,
    # ChatgptIntegration,
    BardIntegration,
)

urlpatterns = [
    path("send-message/", SendMessageView.as_view(), name="send-message"),
    # path("gptproject/", ChatgptIntegration.as_view(), name="gptproject"),
    path("bardproject/", BardIntegration.as_view(), name="bardproject"),
]
