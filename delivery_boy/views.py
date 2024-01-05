from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import (
    DeliveryPostSerializer,
    LocationSerializer,
    DeliveryPersonSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from .models import DeliveryPerson
from django.contrib.gis.geos import Point
from cloudinary import uploader
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from user_panel.models import DeliveryNotification,ShoppingDeliveryPerson,Shopping
from user_panel.serializers import DeliveryNotificationSerializer,ShoppingSerializer



permission_classes([IsAuthenticated])
class DeliveryBoyCrud(APIView):
    def post(self, request):
        print("llllllllllll")
        serializer = DeliveryPostSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            locserializer = LocationSerializer(data=request.data)
            if locserializer.is_valid():
                location = Point(
                    locserializer.validated_data.get("longitude"),
                    locserializer.validated_data.get("latitude"),
                    srid=4326,
                )
                profile_photo = request.data.get("profile_photo")
                res = uploader.upload(profile_photo)
                id_proof = request.data.get("id_proof")
                res1 = uploader.upload(id_proof)
                # DeliveryPerson.objects.create(
                #     user=user,
                #     full_name=serializer.validated_data.get("full_name"),
                #     location=location,
                #     address=serializer.validated_data.get("address"),
                #     delivery_area=serializer.validated_data.get("delivery_area"),
                #     profile_photo=res["url"],
                #     id_proof=res1["url"],
                # )
                return Response(
                    {"msg": "account created sucessfully"}, status=status.HTTP_200_OK
                )
            return Response(locserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            delivery_person = DeliveryPerson.objects.get(user=request.user)
        except:
            return Response(
                {"msg": "delivery person account not fount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DeliveryPersonSerializer(
            delivery_person, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            delivery_person = DeliveryPerson.objects.get(user=request.user)
        except:
            return Response(
                {"msg": "You are not a delivery person"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DeliveryPostSerializer(delivery_person)
        return Response(serializer.data, status=status.HTTP_200_OK)


permission_classes([IsAuthenticated])
class ListNewOrdersNotifiactionOfDelivery(APIView):
    def get(self,request):

        notifications = DeliveryNotification.objects.filter(delivery_person__user_id=2)
        not_serializer = DeliveryNotificationSerializer(notifications,many=True)
        shop_objs = Shopping.objects.filter(
            payment_id__in=notifications.values_list(
                'shooping_payment_id',
                flat=True
                ))
        shop_serializer = ShoppingSerializer(shop_objs,many=True)
        return Response({ 
            'notification':not_serializer.data,
            'shopping':shop_serializer.data
                         },status=status.HTTP_200_OK)


# Create your views here.
