from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import OwnerSerializer,HotelAccountSeriallizer
from accounts.utils import send_email
from .models import HotelOwner,HotelsAccount
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MyUser



@permission_classes([IsAuthenticated])
class OwnerAccountView(APIView):
    def post(self,request):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            owner = HotelOwner.objects.create(
                first_name = serializer.validated_data.get('first_name'),
                last_name = serializer.validated_data.get('last_name'),
                email = serializer.validated_data.get('email'),
                contact = serializer.validated_data.get('contact'),
                id_proof = serializer.validated_data.get('id_proof'),
                id_number = serializer.validated_data.get('id_number')
            )
            owner.user = user
            subject = "You have a message"
            message = "Created the owner account continue and register your hotel"
            email = serializer.validated_data.get('email')
            send_email(email=email,subject=subject,message=message)
            return Response({'msg':'Account created...'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request):
        serializer = OwnerSerializer(HotelOwner,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@permission_classes([IsAuthenticated])
class HotelAccountRegister(APIView):
    def patch(self,request):
        try:
            owner = HotelOwner.objects.get(user=request.user)
            hotel = HotelsAccount.objects.get(owner=owner)
            serializer = HotelAccountSeriallizer(HotelsAccount,request.data,partial=True)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                phone = serializer.validated_data.get('phone')
                if not hotel.is_approved:
                    message = "Your Request for adding your hotel is send successfully, we will respond as fast as we can."
                    subject = "partner with hungry_hub"
                    send_email(message=message,subject=subject,email=email)
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Register owner form first...'},status=status.HTTP_400_BAD_REQUEST)
            





# Create your views here.
