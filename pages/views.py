from hotel_panel.models import HotelsAccount, FoodMenu
from hotel_panel.serializer import HotelAccountSeriallizer, FoodmenuSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q

# from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from accounts.models import SavedLocations
from accounts.serializers import SavedLocationSerializer


class SearchLocation(APIView):
    def get(self, request):
        q = request.GET.get("q")
        if q:
            queryset = SavedLocations.objects.filter(
                Q(city__icontains=q) | Q(district__icontains=q) | Q(state__icontains=q)
            ).values()
            if queryset:
                serializer = SavedLocationSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"msg": "no location available"}, status=status.HTTP_200_OK)


class FilterNearHotels(APIView):
    def get(self, request):
        latitude = request.query_params.get("latitude")
        longitude = request.query_params.get("longitude")
        if latitude is None or longitude is None:
            return Response(
                {
                    "error": "Latitude and longitude are required in the query parameters"
                },
                status=400,
            )

        # nearby_food_menus = FoodMenu.objects.filter(hotel__location__distance_lte=(user_location, D(km=4)),is_available=True)
        # nearby_food_menus = nearby_food_menus.annotate(
        #     distance=Distance('hotel__location', user_location)
        # ).order_by('distance')
        # nearby_food_menus = FoodMenu.objects.filter(
        #     hotel__location__distance_lte=(user_location, D(km=40)),
        #     is_available=True
        #     ).annotate(
        #     distance=Distance('hotel__location', user_location)
        #     ).order_by('distance')
        # serializer = FoodmenuSerializer(nearby_food_menus,many=True)

        try:
            user_location = Point(float(longitude), float(latitude), srid=4326)

            nearby_hotels = (
                HotelsAccount.objects.filter(
                    location__distance_lte=(user_location, D(km=40)), is_approved=True
                )
                .annotate(food_item_count=Count("foodmenu"))
                .filter(food_item_count__gt=0)
            )
            serializer = HotelAccountSeriallizer(nearby_hotels, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"msg": "something wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class FoodsOfSelectedHotel(APIView):
    def get(self, request):
        id = request.GET.get("id")
        print(id)
        if Q(id) & Q(int(id) > 0):
            print(HotelsAccount.objects.get(id=id))
            foods = FoodMenu.objects.filter(Q(hotel__id=id) & Q(is_available=True))
            print(foods)
            serializer = FoodmenuSerializer(foods, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "No hotel with this id"})


# Create your views here.
