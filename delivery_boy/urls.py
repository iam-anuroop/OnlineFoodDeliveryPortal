from django.urls import path
from .views import (
    DeliveryBoyCrud
)


urlpatterns = [
    path('deliverypartner/',DeliveryBoyCrud.as_view(),name='deliverypartner'),
]

