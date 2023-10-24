from django.urls import path
from .views import OwnerAccountView,HotelAccountRegister

urlpatterns = [
    path('owner/',OwnerAccountView.as_view(),name='owner'),
    path('hotel/',HotelAccountRegister.as_view(),name='hotel'),
]