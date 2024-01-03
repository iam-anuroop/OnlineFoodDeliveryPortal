from django.urls import path
from .views import (
    AdminHotelManage,
    AdminPanelApprovedHotels,
    AdminPanelUsersList,
    HotelSearch,
    AdminPanelDeliveryPersonManage,
    AdminPanelDeliveryPersonGet
)

urlpatterns = [
    path("adminhotel/", AdminHotelManage.as_view(), name="adminhotel"),
    path("adminapprovedhotels/",AdminPanelApprovedHotels.as_view(),name="adminapprovedhotels",),
    path("adminuserslist/", AdminPanelUsersList.as_view(), name="adminuserslist"),
    path("hotelsearch/", HotelSearch.as_view(), name="hotelsearch"),
    path("deliveryperson/", AdminPanelDeliveryPersonManage.as_view(), name="deliveryperson"),
    path("getdelivery/", AdminPanelDeliveryPersonGet.as_view(), name="getdelivery"),
]
