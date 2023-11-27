# from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import authenticate
from .serializers import UserSerilaizer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import (
    MyUser ,
    UserProfile
    )
from hotel_panel.models import FoodMenu
from ipware import get_client_ip
import json, urllib
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from django.db.models import F, Count ,Sum ,When ,IntegerField,Case
import json



class UserCurrentLocation(APIView):

    @swagger_auto_schema(
        tags=["Current Location"],
        operation_description="Getting location of user using client ip",
        responses={
            200:"okay",
            400:"errors"
        }
    )
    def post(self,request):
        client_ip, is_routable = get_client_ip(request)
        if is_routable:
            ip_type = 'public'
        else:
            ip_type = 'private'
        client_ip = "103.42.196.132"
        auth = config('FIND_IP_AUTH')
        url = "https://api.ipfind.com/?auth="+auth+"&ip="+client_ip
        resp = urllib.request.urlopen(url)
        data1 = json.loads(resp.read())
        data1['client_ip'] = client_ip
        data1['ip_type'] = ip_type
        return Response(data1,status=status.HTTP_200_OK)



@permission_classes([IsAuthenticated])
class ProfileManage(APIView):

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile getting",
        responses={
            200:UserSerilaizer,
            400:"errors"
        }
    )
    def get(self,request):
        currentuser = request.user
        user = MyUser.objects.get(id=currentuser.id)
        serializer = UserSerilaizer(user)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile Updating",
        responses={
            200:UserSerilaizer,
            400:"errors"
        }
    )
    def patch(self,request):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile:
                serializer = UserSerilaizer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # UserProfile.objects.create(user=user)
            # serializer = UserSerilaizer(user, data=request.data, partial=True)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'msg':'something wrong...'}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile Deleting",
        responses={
            200:"Okay",
            400:"errors"
        }
    )
    def delete(self,request):
        user = request.user
        user.delete()
        return Response({'msg':'Account deleted...'},status=status.HTTP_200_OK)






@permission_classes([IsAuthenticated])
class AddToCart(APIView):
    def post(self, request):
        try:
            cart = request.data.get('cart')
            profile = UserProfile.objects.get(user=request.user)

            if len(cart[0]) == 1:
                key = list(cart[0].keys())[0]
                if profile.cart[0].get(key) is not None:
                    profile.cart[0][key] = profile.cart[0][key] + 1
                else:
                    profile.cart[0][key] = 1
            else:
                profile.cart = cart
            profile.save()
            return Response({"msg": "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":"error while add to cart"},status=status.HTTP_400_BAD_REQUEST)
    


    @permission_classes([IsAuthenticated])
    def get(self,request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            cart_items = profile.cart[0]
            food_item_ids = list(cart_items.keys())
            food_item_counts = list(cart_items.values())
            cart_food_items = FoodMenu.objects.filter(id__in=food_item_ids)


            cart_food_items = cart_food_items.annotate(
                cart_item_count=Case(
                    *[When(id=item_id, then=count) for item_id, count in zip(food_item_ids,food_item_counts)],
                    default=0,
                    output_field=IntegerField()
                )
            ).values()
            print('helloo')
            # x=json.dumps(cart_food_items)
            return Response(cart_food_items)
        except Exception as e:
            return Response({'hi':'error'})

        




# Create your views here.
