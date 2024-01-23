from django.urls import path
from .views import (
    OwnerAccountView,
    HotelAccountRegister,
    VerifyHotelPhone,
    HotelAccountLogin,
    HotelLoginOtp,
    FoodmenuView,
    HotelPhoneOtp,
    HotelProfileView,
    ProgressDetails,
)

urlpatterns = [
    path("owner/", OwnerAccountView.as_view(), name="owner"),
    path("hotel/", HotelAccountRegister.as_view(), name="hotel"),
    path("hotelphone/", VerifyHotelPhone.as_view(), name="hotelphone"),
    path("hotelotp/", HotelLoginOtp.as_view(), name="hotelotp"),
    path("hotellogin/", HotelAccountLogin.as_view(), name="hotellogin"),
    path("hotelphoneotp/", HotelPhoneOtp.as_view(), name="hotelphoneotp"),
    path("hotelprofile/", HotelProfileView.as_view(), name="hotelprofile"),
    path("food/", FoodmenuView.as_view(), name="food"),
    path("track/", ProgressDetails.as_view(), name="track"),
]
