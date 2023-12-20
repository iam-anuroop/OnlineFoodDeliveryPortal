from django.urls import path
from .views import (
    ProfileManage, 
    UserCurrentLocation, 
    AddToCart, 
    PaymentView, 
    AddressManage
    )

urlpatterns = [
    path("profile/", ProfileManage.as_view(), name="profile"),
    path("currentloc/", UserCurrentLocation.as_view(), name="currentloc"),
    path("address/", AddressManage.as_view(), name="address"),
    path("addtocart/", AddToCart.as_view(), name="addtocart"),
    path("payment/", PaymentView.as_view(), name="payment"),
]
