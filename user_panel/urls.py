from django.urls import path
from .views import (
    ProfileManage,
    UserCurrentLocation,
    AddToCart,
    PaymentView,
    PaymentSuccessView,
    AddressManage,
    AllOrdersOfUser,
    OrderDetails,
    OrderTrackingUpdation,
)

urlpatterns = [
    path("profile/", ProfileManage.as_view(), name="profile"),
    path("currentloc/", UserCurrentLocation.as_view(), name="currentloc"),
    path("address/", AddressManage.as_view(), name="address"),
    path("addtocart/", AddToCart.as_view(), name="addtocart"),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("success/", PaymentSuccessView.as_view(), name="success"),
    path("allorders/", AllOrdersOfUser.as_view(), name="allorders"),
    path("orderdetails/", OrderDetails.as_view(), name="orderdetails"),
    path("ordertrack/", OrderTrackingUpdation.as_view(), name="ordertrack"),
]
