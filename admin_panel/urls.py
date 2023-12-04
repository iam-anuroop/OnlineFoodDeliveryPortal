from django.urls import path
from .views import (
    AdminHotelManage,
    AdminPanelApprovedHotels,
    AdminPanelUsersList,
    HotelSearch
                    )

urlpatterns = [
    path('adminhotel/',AdminHotelManage.as_view(),name='adminhotel'),
    path('adminapprovedhotels/',AdminPanelApprovedHotels.as_view(),name='adminapprovedhotels'),
    path('adminuserslist/',AdminPanelUsersList.as_view(),name='adminuserslist'),
    path('hotelsearch/',HotelSearch.as_view(),name='hotelsearch'),
]
