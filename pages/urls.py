from django.urls import path
from .views import (
    FilterNearHotels,
    SearchLocation,
    FoodsOfSelectedHotel,
)


urlpatterns = [
    path("nearfood/", FilterNearHotels.as_view(), name="nearfood"),
    path("searchlocation/", SearchLocation.as_view(), name="searchlocation"),
    path("hotelfoods/", FoodsOfSelectedHotel.as_view(), name="hotelfoods"),
]
