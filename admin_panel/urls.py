from django.urls import path
from .views import (
    AdminHotelManage
                    )

urlpatterns = [
    path('adminhotel/',AdminHotelManage.as_view(),name='adminhotel'),
]
