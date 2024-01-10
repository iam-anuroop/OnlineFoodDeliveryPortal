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
from user_panel.models import DeliveryNotification, Shopping
from user_panel.serializers import DeliveryNotificationSerializer, ShoppingSerializer
from hotel_panel.models import HotelsAccount
from hotel_panel.serializer import HotelAccountSeriallizer


@permission_classes([IsAuthenticated])
class DeliveryBoyCrud(APIView):
    def post(self, request):
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
                DeliveryPerson.objects.create(
                    user=user,
                    full_name=serializer.validated_data.get("full_name"),
                    location=location,
                    address=serializer.validated_data.get("address"),
                    delivery_area=serializer.validated_data.get("delivery_area"),
                    profile_photo=res["url"],
                    id_proof=res1["url"],
                )
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


@permission_classes([IsAuthenticated])
class ListNewOrdersNotifiactionOfDelivery(APIView):
    def get(self, request):
        notifications = DeliveryNotification.objects.filter(delivery_person__user=request.user,status=None)
        not_serializer = DeliveryNotificationSerializer(notifications, many=True)
        shop_objs = Shopping.objects.filter(
            payment_id__in=notifications.values_list("shooping_payment_id", flat=True)
        )
        shop_serializer = ShoppingSerializer(shop_objs, many=True)
        return Response(
            {"notification": not_serializer.data, "shopping": shop_serializer.data},
            status=status.HTTP_200_OK,
        )


@permission_classes([IsAuthenticated])
class AcceptRejectOrders(APIView):
    def post(self,request):
        action = request.data.get('data')
        del_id = request.data.get('del_id')
        notification = DeliveryNotification.objects.get(id=del_id)
        if action == True: 
            notification.status='accepted'
        else :
            notification.status='rejected'
        notification.save()

        return Response({'msg':'accpted the delivery'},status=status.HTTP_200_OK)



@permission_classes([IsAuthenticated])
class CurrentOrders(APIView):
    def get(self,request):
        orders = DeliveryNotification.objects.filter(delivery_person__user=request.user,status='accepted')
        serializer = DeliveryNotificationSerializer(orders,many=True)
        payment_id = orders.values_list()
        print(payment_id)
        # Shopping.objects.filter(payment_id==payment_id)
        # print
        # hot_det = HotelsAccount.objects.filter(id__in=Shopping.objects.filter(
        #         payment_id = payment_id).values_list('id',flat=True).first())
        # print(hot_det)
        return Response(serializer.data,status=status.HTTP_200_OK)




# Create your views here.
