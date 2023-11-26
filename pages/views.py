from django.shortcuts import render
from hotel_panel.models import HotelOwner,HotelsAccount,FoodMenu
from hotel_panel.serializer import HotelAccountSeriallizer,FoodmenuSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D



class FilterNearHotels(APIView):
    def get(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        user_location = Point(float(longitude), float(latitude), srid=4326)
        nearby_food_menus = FoodMenu.objects.filter(hotel__location__distance_lte=(user_location, D(km=4)),is_available=True)
        nearby_food_menus = nearby_food_menus.annotate(
            distance=Distance('hotel__location', user_location)
        ).order_by('distance')
        serializer = FoodmenuSerializer(nearby_food_menus,many=True)
        return Response(serializer.data)




# Create your views here.
