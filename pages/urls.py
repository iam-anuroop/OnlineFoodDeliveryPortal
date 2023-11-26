from django.urls import path
from .views import (
    FilterNearHotels
)


urlpatterns = [
    path('nearfood/',FilterNearHotels.as_view(),name='nearfood'),
]