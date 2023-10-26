from django.urls import path
from .views import OwnerAccountView,HotelAccountRegister,VerifyHotelPhone,HotelAccountLogin,HotelLoginOtp,HotelLogout,Checkkkkk

urlpatterns = [
    path('owner/',OwnerAccountView.as_view(),name='owner'),
    path('hotel/',HotelAccountRegister.as_view(),name='hotel'),
    path('hotelphone/',VerifyHotelPhone.as_view(),name='hotelphone'),
    path('hotelotp/',HotelLoginOtp.as_view(),name='hotelotp'),
    path('hotellogin/',HotelAccountLogin.as_view(),name='hotellogin'),
    path('hotellogout/',HotelLogout.as_view(),name='hotellogout'),
    path('check/',Checkkkkk.as_view(),name='check'),
]