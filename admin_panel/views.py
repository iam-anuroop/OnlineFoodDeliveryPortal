from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
from hotel_panel.models import HotelsAccount
from accounts.models import UserProfile
from user_panel.serializers import UserSerilaizer
from hotel_panel.serializer import HotelAccountSeriallizer
from django.db.models import Q



@permission_classes([IsAdminUser])
class AdminHotelManage(APIView):
    def post(self,request):
        hotel_email = request.data.get('hotel_email')
        try:
            hotel = HotelsAccount.objects.get(email = hotel_email)
            hotel.is_approved = True
            hotel.save()
        except Exception as e:
            return Response({'msg':'no hotel with this mail'},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        data = request.data.get('data')
        if data == 'users':
            res = self.get_users()
        if data == 'hotels':
            res = self.get_hotels()
        if data == 'unapproved_hotels':
            res = self.get_unApprovedHotels()
        if res['status']=='ok':
            return Response(res,status=status.HTTP_200_OK)
        return Response(res,status=status.HTTP_400_BAD_REQUEST) 
    
    def get_users():
        users = UserProfile.objects.all()
        serializer = UserSerilaizer(users,many=True)
        if serializer.is_valid():
            return {'data':serializer.data,'status':'ok'}
        return serializer.errors
        
    def get_hotels():
        hotels = HotelsAccount.objects.filter(Q(is_active=True) & Q(is_approved = True))
        serializer = HotelAccountSeriallizer(hotels,many=True)
        if serializer.is_valid():
            return {'data':serializer.data,'status':'ok'}
        return serializer.errors
        
    def get_unApprovedHotels():
        hotels = HotelsAccount.objects.filter(Q(is_active=True) & Q(is_approved = False))
        serializer = HotelAccountSeriallizer(hotels,many=True)
        if serializer.is_valid():
            return {'data':serializer.data,'status':'ok'}
        return serializer.errors



# Create your views here.
