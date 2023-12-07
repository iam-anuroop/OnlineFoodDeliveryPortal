from django.urls import path
from .views import ProfileManage, UserCurrentLocation, AddToCart, PaymentView

urlpatterns = [
    path("profile/", ProfileManage.as_view(), name="profile"),
    path("currentloc/", UserCurrentLocation.as_view(), name="currentloc"),
    path("addtocart/", AddToCart.as_view(), name="addtocart"),
    path("payment/", PaymentView.as_view(), name="payment"),
]
