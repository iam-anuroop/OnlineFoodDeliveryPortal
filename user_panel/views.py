# from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# from django.contrib.auth import authenticate
from .serializers import UserSerilaizer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import MyUser, UserProfile, SavedLocations
from user_panel.serializers import UserProfileSerializer
from hotel_panel.models import FoodMenu
from hotel_panel.serializer import FoodmenuSerializer
from ipware import get_client_ip
import json, urllib
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q, F, Count, Sum, When, IntegerField, Case
import json
from django.contrib.gis.geos import Point
import stripe
from django.conf import settings
from django.shortcuts import redirect


class UserCurrentLocation(APIView):
    @swagger_auto_schema(
        tags=["Current Location"],
        operation_description="Getting location of user using client ip",
        responses={200: "okay", 400: "errors"},
    )
    def post(self, request):
        client_ip, is_routable = get_client_ip(request)
        if is_routable:
            ip_type = "public"
        else:
            ip_type = "private"
        client_ip = "103.42.196.132"
        auth = config("FIND_IP_AUTH")
        url = "https://api.ipfind.com/?auth=" + auth + "&ip=" + client_ip
        resp = urllib.request.urlopen(url)
        data1 = json.loads(resp.read())
        data1["client_ip"] = client_ip
        data1["ip_type"] = ip_type

        if (
            Q(data1["country"])
            & Q(data1["city"])
            & Q(data1["region"])
            & Q(data1["county"])
        ):
            location = Point(data1["longitude"], data1["latitude"], srid=4326)

            if not SavedLocations.objects.filter(
                Q(country=data1["country"])
                & Q(city=data1["city"])
                & Q(state=data1["region"])
                & Q(district=data1["county"])
            ).exists():
                SavedLocations.objects.create(
                    country=data1["country"],
                    state=data1["region"],
                    district=data1["county"],
                    city=data1["city"],
                    location=location,
                )
        return Response(data1, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class ProfileManage(APIView):
    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile getting",
        responses={200: UserSerilaizer, 400: "errors"},
    )
    def get(self, request):
        currentuser = request.user
        user = MyUser.objects.get(id=currentuser.id)
        serializer = UserSerilaizer(user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile Updating",
        responses={200: UserSerilaizer, 400: "errors"},
    )
    def patch(self, request):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile:
                serializer = UserSerilaizer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"data": serializer.data}, status=status.HTTP_200_OK
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # UserProfile.objects.create(user=user)
            # serializer = UserSerilaizer(user, data=request.data, partial=True)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(
                {"msg": "something wrong..."}, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile Deleting",
        responses={200: "Okay", 400: "errors"},
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"msg": "Account deleted..."}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class AddToCart(APIView):
    def post(self, request):
        try:
            hotel = str(request.data.get("hotel"))
            item = str(request.data.get("item"))
            count = request.data.get("count")
            cart = request.data.get("cart")
            profile = UserProfile.objects.get(user=request.user)

            if cart is not None:
                x = [{hotel: cart}]
                profile.cart = x
                profile.save()
            else:
                if profile.cart is not None:
                    try:
                        if profile.cart[0][hotel]:
                            if profile.cart[0][hotel][0][item]:
                                profile.cart[0][hotel][0][item] = int(
                                    profile.cart[0][hotel][0][item]
                                ) + int(count)
                                if int(profile.cart[0][hotel][0][item]) < 1:
                                    del profile.cart[0][hotel][0][item]
                                if len(profile.cart[0][hotel][0]) < 1:
                                    profile.cart = None
                            else:
                                profile.cart[0][hotel][0][item] = 1
                        else:
                            if len(profile.cart[0]) > 0:
                                x = [{hotel: [{item: 1}]}]
                                profile.cart = x
                    except:
                        x = [{hotel: [{item: 1}]}]
                        profile.cart = x
                else:
                    x = [{hotel: [{item: 1}]}]
                    profile.cart = x

            profile.save()

            return Response({"msg": "cart updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, "lllll")
            return Response(
                {"msg": "error while add to cart"}, status=status.HTTP_400_BAD_REQUEST
            )

    @permission_classes([IsAuthenticated])
    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            if profile.cart is not None:
                cart_items = profile.cart[0][list(profile.cart[0].keys())[0]][0]
                food_item_ids = list(cart_items.keys())
                food_item_counts = list(cart_items.values())
                cart_food_items = (
                    FoodMenu.objects.filter(id__in=food_item_ids)
                    .annotate(
                        cart_item_count=Case(
                            *[
                                When(id=item_id, then=count)
                                for item_id, count in zip(
                                    food_item_ids, food_item_counts
                                )
                            ],
                            default=0,
                            output_field=IntegerField()
                        )
                    )
                    .values()
                )

                # serializer = FoodmenuSerializer(cart_food_items,many=True)
                return Response(
                    {"cart_food_items": cart_food_items, "profile": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"cart_food_items": [], "profile": serializer.data},
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                {"msg": "Something wrong"}, status=status.HTTP_400_BAD_REQUEST
            )



stripe.api_key = config('STRIPE_CLIENT_SECRET')
@permission_classes([IsAuthenticated])
class PaymentView(APIView):
    def post(self,request):
        print(request.user)
        try:
            
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1OLLqMSGhzZ6Pyhpl5B4CUg5',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url= settings.FRONT_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url= settings.FRONT_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            return Response({'msg':'somthing went wrong on stripe'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here.
