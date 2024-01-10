from django.urls import path
from .views import (
    DeliveryBoyCrud, 
    ListNewOrdersNotifiactionOfDelivery,
    AcceptRejectOrders,
    CurrentOrders
    )


urlpatterns = [
    path("deliverypartner/", DeliveryBoyCrud.as_view(), name="deliverypartner"),
    path("ordernotification/",ListNewOrdersNotifiactionOfDelivery.as_view(),name="ordernotification",),
    path("acceptrejectorders/", AcceptRejectOrders.as_view(), name="acceptrejectorders"),
    path("currentorders/", CurrentOrders.as_view(), name="currentorders"),
]
