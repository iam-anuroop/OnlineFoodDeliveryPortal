from django.urls import path
from .views import ProfileManage,UserCurrentLocation

urlpatterns = [
    path('profile/',ProfileManage.as_view(),name='profile'),
    path('currentloc/',UserCurrentLocation.as_view(),name='currentloc'),
]
